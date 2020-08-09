link = "/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&adId=A093930128AWNHNP1YCIF&url=%2FVivo-Storage-Additional-Exchange-Offers%2Fdp%2FB086KDZGTZ%2Fref%3Dsr_1_2_sspa%3Fdchild%3D1%26keywords%3Dmobile%26qid%3D1596991258%26sr%3D8-2-spons%26psc%3D1&qualifier=1596991258&id=2477743919507353&widgetName=sp_atf"
asin = None
if '.html' in link:
    asin = link[link.find('%2Fdp%2F')+8:link.find('%2Fref')]

print(asin)
