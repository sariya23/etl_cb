-- +goose Up
-- +goose StatementBegin
alter table currency_course rename to currenct_rate;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
alter table currenct_rate rename to currency_course;
-- +goose StatementEnd
