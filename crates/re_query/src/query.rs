use polars_core::prelude::*;
use re_arrow_store::{DataStore, TimelineQuery};
use re_log_types::{field_types::Instance, msg_bundle::Component, ComponentName, ObjPath};

#[derive(thiserror::Error, Debug)]
pub enum QueryError {
    #[error("Tried to access a column that doesn't exist")]
    BadAccess,

    #[error("Could not find primary")]
    PrimaryNotFound,

    #[error("Error executing Polars Query")]
    PolarsError(#[from] PolarsError),
}

pub type Result<T> = std::result::Result<T, QueryError>;

/// Retrieves a [`DataFrame`] for a [`Component`] with its corresponding
/// [`Instance`] values.
/// ```
/// # use re_arrow_store::{TimelineQuery, TimeQuery};
/// # use re_log_types::{Timeline, field_types::Point2D, msg_bundle::Component};
/// # let store = re_query::__populate_example_store();
///
/// let ent_path = "point";
/// let timeline_query = TimelineQuery::new(
///   Timeline::new_sequence("frame_nr"),
///   TimeQuery::LatestAt(123.into()),
/// );
///
/// let df = re_query::get_component_with_instances(
///   &store,
///   &timeline_query,
///   &ent_path.into(),
///   Point2D::name(),
/// )
/// .unwrap();
///
/// println!("{:?}", df);
/// ```
///
/// Outputs:
/// ```text
/// ┌──────────┬───────────┐
/// │ instance ┆ point2d   │
/// │ ---      ┆ ---       │
/// │ u64      ┆ struct[2] │
/// ╞══════════╪═══════════╡
/// │ 42       ┆ {1.0,2.0} │
/// ├╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┤
/// │ 96       ┆ {3.0,4.0} │
/// └──────────┴───────────┘
/// ```
///
pub fn get_component_with_instances(
    store: &DataStore,
    timeline_query: &TimelineQuery,
    ent_path: &ObjPath,
    component: ComponentName,
) -> Result<DataFrame> {
    let components = [Instance::name(), component];

    let row_indices = store
        .query(timeline_query, ent_path, component, &components)
        .ok_or(QueryError::PrimaryNotFound)?;

    let results = store.get(&components, &row_indices);

    let series: Result<Vec<Series>> = components
        .iter()
        .zip(results)
        .filter_map(|(component, col)| col.map(|col| (component, col)))
        .map(|(&component, col)| Ok(Series::try_from((component.as_str(), col))?))
        .collect();

    DataFrame::new(series?).map_err(Into::into)
}

/// If a `DataFrame` has no `Instance` column create one from the row numbers
fn add_instances_and_sort_if_needed(df: &DataFrame) -> Result<DataFrame> {
    let instance_name = Instance::name().as_str();
    if df.column(instance_name).is_ok() {
        // If we have an InstanceKey column already, make sure that it's sorted.
        // TODO(jleibs): can remove this once we have a sort guarantee from the store
        let reverse = false;
        Ok(df.sort([instance_name], reverse)?)
    } else {
        // If we don't have an InstanceKey column, it is implicit, and we generate it
        // based on the row-number so we can use this in join-operations.
        // The default Polars row type is u32 and so we need to convert it to the
        // expected type of our InstanceKeys.
        let mut with_rows = df.with_row_count(instance_name, None)?;
        let rows = with_rows.select_at_idx(0).ok_or(QueryError::BadAccess)?;
        let u64_rows = rows.cast(&DataType::UInt64)?;
        with_rows.replace_at_idx(0, u64_rows).unwrap();
        Ok(with_rows)
    }
}

/// Retrieve an entity as a polars Dataframe
///
/// An entity has a primary [`Component`] which is expected to always be
/// present. The length of the batch will be equal to the length of the primary
/// component.
///
/// The remaining components are joined based on their instances. If those not
/// available, they are implicitly treated as an integer sequence of the correct
/// length.
///
/// ```
/// # use re_arrow_store::{TimelineQuery, TimeQuery};
/// # use re_log_types::{Timeline, field_types::{Point2D, ColorRGBA}, msg_bundle::Component};
/// # let store = re_query::__populate_example_store();
///
/// let ent_path = "point";
/// let timeline_query = TimelineQuery::new(
///   Timeline::new_sequence("frame_nr"),
///   TimeQuery::LatestAt(123.into()),
/// );
///
/// let df = re_query::query_entity_with_primary(
///   &store,
///   &timeline_query,
///   &ent_path.into(),
///   Point2D::name(),
///   &[ColorRGBA::name()],
/// )
/// .unwrap();
///
/// println!("{:?}", df);
/// ```
///
/// Outputs:
/// ```text
/// ┌──────────┬───────────┬────────────┐
/// │ instance ┆ point2d   ┆ colorrgba  │
/// │ ---      ┆ ---       ┆ ---        │
/// │ u64      ┆ struct[2] ┆ u32        │
/// ╞══════════╪═══════════╪════════════╡
/// │ 42       ┆ {1.0,2.0} ┆ null       │
/// ├╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌┤
/// │ 96       ┆ {3.0,4.0} ┆ 4278190080 │
/// └──────────┴───────────┴────────────┘
/// ```
///
pub fn query_entity_with_primary<const N: usize>(
    store: &DataStore,
    timeline_query: &TimelineQuery,
    ent_path: &ObjPath,
    primary: ComponentName,
    components: &[ComponentName; N],
) -> Result<DataFrame> {
    let df = get_component_with_instances(store, timeline_query, ent_path, primary)?;

    // TODO(jleibs): lots of room for optimization here. Once "instance" is
    // guaranteed to be sorted we should be able to leverage this during the
    // join. Series have a SetSorted option to specify this. join_asof might be
    // the right place to start digging.

    let df = add_instances_and_sort_if_needed(&df);

    let instance_name = Instance::name().as_str();
    let joined = components
        .iter()
        .fold(df, |df: Result<DataFrame>, &component| {
            // If we find the component, then we try to left-join with the existing dataframe
            // If the column we are looking up isn't found, just return the dataframe as is
            // For any other error, escalate
            match get_component_with_instances(store, timeline_query, ent_path, component) {
                Ok(component_df) => {
                    let component_df = add_instances_and_sort_if_needed(&component_df)?;
                    // We use an asof join which takes advantage of the fact
                    // that our join-columns are sorted. The strategy shouldn't
                    // matter here since we have a Tolerance of None.
                    let joined = df?.join_asof(
                        &component_df,
                        instance_name,
                        instance_name,
                        AsofStrategy::Backward,
                        None,
                        None,
                    );
                    Ok(joined?)
                }
                Err(QueryError::PrimaryNotFound) => df,
                Err(err) => Err(err),
            }
        });

    joined
}

/// Helper used to create an example store we can use for querying in doctests
pub fn __populate_example_store() -> DataStore {
    use re_log_types::{
        datagen::build_frame_nr,
        field_types::{ColorRGBA, Point2D},
        msg_bundle::try_build_msg_bundle2,
        MsgId,
    };

    let mut store = DataStore::default();

    let ent_path = "point";
    let timepoint = [build_frame_nr(123)];

    let instances = vec![Instance(42), Instance(96)];
    let points = vec![Point2D { x: 1.0, y: 2.0 }, Point2D { x: 3.0, y: 4.0 }];

    let bundle =
        try_build_msg_bundle2(MsgId::ZERO, ent_path, timepoint, (&instances, &points)).unwrap();
    store.insert(&bundle).unwrap();

    let instances = vec![Instance(96)];
    let colors = vec![ColorRGBA(0xff000000)];
    let bundle =
        try_build_msg_bundle2(MsgId::ZERO, ent_path, timepoint, (instances, colors)).unwrap();
    store.insert(&bundle).unwrap();

    store
}

#[test]
fn component_with_instances() {
    use crate::dataframe_util::df_builder2;
    use re_arrow_store::{TimeQuery, TimelineQuery};
    use re_log_types::{field_types::Point2D, msg_bundle::Component as _, Timeline};

    let store = __populate_example_store();

    let ent_path = "point";
    let timeline_query = TimelineQuery::new(
        Timeline::new_sequence("frame_nr"),
        TimeQuery::LatestAt(123.into()),
    );

    let df =
        get_component_with_instances(&store, &timeline_query, &ent_path.into(), Point2D::name())
            .unwrap();
    //eprintln!("{:?}", df);

    let instances = vec![Some(Instance(42)), Some(Instance(96))];
    let points = vec![
        Some(Point2D { x: 1.0, y: 2.0 }),
        Some(Point2D { x: 3.0, y: 4.0 }),
    ];

    let expected = df_builder2(&instances, &points).unwrap();

    assert_eq!(df, expected);
}
