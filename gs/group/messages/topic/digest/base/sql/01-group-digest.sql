SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

-- The table that records when a digest went out to the group members.
CREATE TABLE group_digest (
    site_id    TEXT                      NOT NULL,
    group_id   TEXT                      NOT NULL,
    sent_date  TIMESTAMP WITH TIME ZONE  NOT NULL DEFAULT NOW(),
    PRIMARY KEY (site_id, group_id, sent_date)
);
