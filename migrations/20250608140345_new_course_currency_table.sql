-- +goose Up
-- +goose StatementBegin
create table if not exists currency_course (
    num_code varchar(3) not null,
    char_code varchar(3) not null,
    nominal smallint not null default 1,
    name varchar(40) not null,
    value decimal not null,
    vunit_value decimal not null,
    course_date date not null,
    primary key (char_code, course_date)
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
drop table if exists currency_course;
-- +goose StatementEnd
