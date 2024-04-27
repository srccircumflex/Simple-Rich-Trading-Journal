
# row record fields:
# (except for `id` and `cat`, all fields can be unset or filled with `None`)
# {
#       id                 <int>
#       cat                <
#                           ''  : undefined
#                           'd' : deposit
#                           'p' : payout
#                           'i' : ITC (Interests, Taxes and other Costs or Income)
#                           'v' : dividend
#                           'tf': finalized trade
#                           'to': open trade
#                          >
#       Name               <str>
#       Symbol             <str>
#       Type               <str>
#       n                  <float>
#       InvestTime         <time_str>
#       InvestAmount       <float>
#       InvestCourse       <float>
#       TakeTime           <time_str>
#       TakeAmount         <float>
#       TakeCourse         <float>
#       ITC                <float>  (Interests, Taxes and other Costs or Income)
#       Performance        <float>
#       Profit             <float>
#       Dividend           <float>
#       Note               <str>
#       HoldTime           <duration_str>
#       Performance/Day    <float>
#       Profit/Day         <float>
# }

def symbol_call(update_data: dict) -> dict:
    # Is called when the cells of columns `Name`, `Symbol` or `Type` are edited.
    # Receives the object `cellValueChanged` (see https://dash.plotly.com/dash-ag-grid/editing-and-callbacks).
    # The return value must represent the row record (as `cellValueChanged`["data"]).
    return update_data["data"]


def course_call(row_record: dict) -> bool:
    # Is called if a record falls into the `Open Trade` category.
    # Receives the row record.
    # The return value indicates whether something has been changed.
    # If something is changed, the record must be edited in place, e.g.:
    #   >>> row_record["TakeCourse"] = your_api(row_record["Symbol"])
    # Furthermore, "TakeCourse" AND "TakeAmount" must be set:
    #   >>> row_record["TakeAmount"] = row_record["TakeCourse"] * row_record["n"]
    return False


def init_log(log_data: list[dict]) -> tuple[list[dict], bool]:
    # Is executed once during initialization.
    # Receives the data of the log memory and must return it,
    # secondly whether this data should be directly written to the disk.
    # Each field in log_data is a row record.
    return log_data, False


def init_history(history_data: dict[int, dict]) -> tuple[dict[int, dict], bool]:
    # Is executed once during initialization.
    # Receives the data of the history memory and must return it,
    # secondly whether this data should be directly written to the disk.
    # history_data: {history_id(int): {"time": seconds_since_epoch(int), "data": [row record, ...]}, ...}
    return history_data, False
