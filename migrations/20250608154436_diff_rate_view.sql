-- +goose Up
-- +goose StatementBegin
create materialized view currency_rate_change_yesterday as
with today as (
    select * from currency_rate where rate_date = (select max(rate_date) from currency_rate)
),
yesterday as (
    select * from currency_rate where rate_date = (
        select max(rate_date)
        from currency_rate
        where rate_date < (select max(rate_date) from currency_rate)
    )
)
select
    t.char_code,
    t.value as last_value,
    y.value as prev_value,
    round(t.value - y.value, 4) as diff,
    round((t.value - y.value) / y.value * 100, 2) as diff_percent
from today t
join yesterday y using(char_code);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop materialized view currency_rate_change_yesterday;
-- +goose StatementEnd