-- +goose Up
-- +goose StatementBegin
create table currency_course (
    currency_course_id bigint generated always as identity primary key,
    currency_id int not null references currency (currency_id)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop table currency_course;
-- +goose StatementEnd
