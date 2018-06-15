CREATE TABLE guba.Gb_Fact_Following_Hist
(
    MongoId varchar(50),
    Operation varchar(20),
    ActionDate date NOT NULL,
    Uid varchar(50),
    FollowedUid varchar(50),
    ActionTime timestamp,
    IsTradeDay int,
    Is4Statictics int,
    RejectReason varchar(50),
    EUTIME timestamp DEFAULT "sysdate"(),
    EID varchar(100),
    EID_kudu varchar(50),
    EID_Vtc numeric(38,0) DEFAULT nextval('guba.Gb_Fact_Following_Hist_Seq'),
    EtlMockFlag int NOT NULL DEFAULT 0,
    InsertFlag int NOT NULL DEFAULT 0
)