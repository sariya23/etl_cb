-- +goose Up
-- +goose StatementBegin
create materialized view avg_currenct_rate_all_time as (
    select char_code, round(avg(value), 2)
    from currency_rate
    group by char_code
    order by char_code
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop materialized view avg_currenct_rate_all_time;
-- +goose StatementEnd
