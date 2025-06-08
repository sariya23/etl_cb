-- +goose Up
-- +goose StatementBegin
create materialized view last_currency_rate as (
    select * from currency_rate
    where rate_date = (select max(rate_date) from currency_rate)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop materialized view last_currency_rate;
-- +goose StatementEnd
