Select C.Symbol,C.Series,C.DateOfListing,C.IsActive,D.CompanyName,
D.FaceValue,D.MarketCap,D.EPS,PE,SharedIssued,Industry,IndexName from Company C 
inner join CompanyDetails D on C.Id = D.CompanyId
left outer join [dbo].[IndexConstituent] IC on C.Symbol = IC.Symbol
left outer join [dbo].[IndexDetails] I on IC.IndexId = I.ID
--truncate table [dbo].[CompanyDetails]



