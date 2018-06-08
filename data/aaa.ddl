
CREATE mulit tempo sql TABLE fff.aaa
(
    _Id varchar(50),
    Operation varchar(20),
    ActionDate date,
    Uid varchar(20),PostId numeric(38,0),
    ReplyUid varchar(20),
    PostFrom int,
    ActionTime timestamp,    IsTradeDay int,
    Is4Statictics int,
    RejectReason varchar(50),    EUTIME timestamp DEFAULT "sysdate"(),
    EID varchar(100),
    EID_kudu varchar(50),
    EID_Vtc numeric(38,0) DEFAULT nextval('guba.Gb_Fact_ReplyLike_Today_Seq'),
    ReplyId numeric(38    ,0),
    BatchID varchar(50));