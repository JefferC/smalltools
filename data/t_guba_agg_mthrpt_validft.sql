truncate table tmp.sisi_Gb_mthRpt_ValidFT_tmp
;
insert /*+ DIRECT,LABEL (BD02006_GUBA_20180301_01)*/ into tmp.sisi_Gb_mthRpt_ValidFT_tmp
	select to_char(publishtime, 'yyyyMmm') as mth,
		date(publishtime) as CalcDay, IsStockDay, ClientType,
		UserID, Country, ShortProvince, ShortCity,
		count(FTID) as FTCnt,
		count(case when FTStatus <> 1 then FTID end) as ValidFTCnt,
		count(case Tag when 1 then FTID end) as TopicCnt,
		count(case when FTStatus <> 1 and Tag=1 then FTID end) as ValidTopicCnt, 
		count(case Tag when 2 then FTID end) as ReplyCnt,
		count(case when FTStatus <> 1 and Tag=2 then FTID end) as ValidReplyCnt
	from (
		select a.publishtime, a.TopicID as FTID, a.UserID, 1 as Tag, 
			CASE e.CaoZuoType WHEN NULLSEQUAL 0::numeric(18,0) THEN 1::numeric(18,0) WHEN NULLSEQUAL 1::numeric(18,0) THEN 0::numeric(18,0) WHEN NULLSEQUAL NULL::numeric(1,0) THEN a.Topic_del ELSE e.CaoZuoType END as FTStatus, 
			IsTradeDay as IsStockDay, 
			a.IP, d.Country, d.ShortProvince, d.ShortCity,
			lower(split_part(b.ProductLineInfo, '-',2)) as ClientType
		from guba.Gb_Stg_Topic a 
		LEFT JOIN guba.Gb_Stg_CaoZuoTopic e ON (a.TopicID = e.TopicID AND a.RecStatus <> 3::numeric(18,0))
		join guba.gb_dim_postfrom b on a.postfrom = b.postfromID
		join common.cmm_dim_date c on date(publishtime) = c.StdDate
		join common.cmm_dim_ip d on inet_aton(a.ip) >= d.sipid and inet_aton(a.ip) <=d.eipid
		where date(publishtime) >= date'?' 
			and date(publishtime) <= date'?'
		union all
		select a.publishtime, a.commentID as FTID, a.UserID, 2 as Tag,
			CASE e.CaoZuoType WHEN NULLSEQUAL 0::numeric(18,0) THEN 1::numeric(18,0) WHEN NULLSEQUAL 1::numeric(18,0) THEN 0::numeric(18,0) WHEN NULLSEQUAL NULL::numeric(1,0) THEN a.CommentStatus ELSE e.CaoZuoType END as FTStatus, 
			IsTradeDay as IsStockDay, 
			a.IP, d.Country, d.ShortProvince, d.ShortCity,
			lower(split_part(b.ProductLineInfo, '-',2)) as ClientType
		from guba.Gb_Stg_Review a LEFT JOIN guba.Gb_Stg_CaoZuoReview e ON (a.CommentID = e.CommentID AND e.RecStatus <> 3::numeric(18,0))
		join guba.gb_dim_postfrom b on a.postfrom = b.postfromID
		join common.cmm_dim_date c on date(publishtime) = c.StdDate
		join common.cmm_dim_ip d on inet_aton(a.ip) >= d.sipid and inet_aton(a.ip) <= d.eipid
		where date(publishtime) >= date'?'
			and date(publishtime) <= date'?'
	) t 
	group by mth, CalcDay, IsStockDay, ClientType, UserID, 
	Country, ShortProvince, ShortCity
