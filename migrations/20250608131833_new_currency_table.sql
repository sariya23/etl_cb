-- +goose Up
-- +goose StatementBegin
create table if not exists currency (
    currency_id int generated always as identity primary key,
    currency_num_code varchar(3) not null unique,
    currenct_char_code varchar(3) not null unique,
    currenct_name varchar(40) not null
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop table currency;
-- +goose StatementEnd
