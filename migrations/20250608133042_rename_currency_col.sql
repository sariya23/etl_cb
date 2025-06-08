-- +goose Up
-- +goose StatementBegin
alter table currency rename column currenct_char_code to currency_char_code;
alter table currency rename column currenct_name to currency_name;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
alter table currency rename column currency_char_code to currenct_char_code;
alter table currency rename column currency_name to currenct_name;
-- +goose StatementEnd
