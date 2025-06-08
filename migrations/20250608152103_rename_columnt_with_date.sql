-- +goose Up
-- +goose StatementBegin
alter table currency_rate rename column course_date to rate_date;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
alter table currency_rate rename column rate_date to course_date;
-- +goose StatementEnd
