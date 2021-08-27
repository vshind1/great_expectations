import warnings

from dateutil.parser import parse

from great_expectations.execution_engine import (
    PandasExecutionEngine,
    SparkDFExecutionEngine,
)
from great_expectations.execution_engine.sqlalchemy_execution_engine import (
    SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.metrics.column_aggregate_metric_provider import (
    ColumnAggregateMetricProvider,
    column_aggregate_partial,
    column_aggregate_value,
)
from great_expectations.expectations.metrics.column_aggregate_metric_provider import (
    sa as sa,
)
from great_expectations.expectations.metrics.import_manager import F


class ColumnMin(ColumnAggregateMetricProvider):
    metric_name = "column.min"

    @column_aggregate_value(engine=PandasExecutionEngine)
    def _pandas(cls, column, parse_strings_as_datetimes=None, **kwargs):
        if parse_strings_as_datetimes:
            temp_column = column.map(parse)
            return temp_column.min()
        else:
            return column.min()

    @column_aggregate_partial(engine=SqlAlchemyExecutionEngine)
    def _sqlalchemy(cls, column, parse_strings_as_datetimes=None, **kwargs):
        if parse_strings_as_datetimes:
            raise NotImplementedError

        return sa.func.min(column)

    @column_aggregate_partial(engine=SparkDFExecutionEngine)
    def _spark(cls, column, parse_strings_as_datetimes=None, **kwargs):
        if parse_strings_as_datetimes:
            raise NotImplementedError

        return F.min(column)
