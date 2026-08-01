# -*- coding: utf-8 -*-
import re, io

h = io.open('kvy-seo-audit-dashboard-v2.html', encoding='utf-8').read()
raw = io.open('kvy-merged-data.csv', encoding='utf-8').read().strip()

h = re.sub(r'var RAW = `[\s\S]*?`;', 'var RAW = `' + raw + '`;', h, count=1)

# parser: thêm sessions GA4 + engagement
old = """  return {p:p,g:+a[1],s:200,t:+a[2],w:+a[3],ld:+a[4],f:+a[5],il:+a[6],im:+a[7],na:+a[8],h1:+a[9],tl:+a[10],dl:+a[11],kb:+a[12],cl:cl,ip:ip,po:po,ctr:ctr,opp:opp};"""
new = """  var se=+a[16]||0, en=a[17]===""||a[17]===undefined?null:+a[17];
  return {p:p,g:+a[1],s:200,t:+a[2],w:+a[3],ld:+a[4],f:+a[5],il:+a[6],im:+a[7],na:+a[8],h1:+a[9],tl:+a[10],dl:+a[11],kb:+a[12],cl:cl,ip:ip,po:po,ctr:ctr,opp:opp,se:se,en:en};"""
assert old in h
h = h.replace(old, new, 1)

# cột mới
oldth = """   <th data-k="cl">Clicks (GSC)</th><th data-k="ip">Impressions</th><th data-k="ctr">CTR</th><th data-k="po">Vị trí TB</th>"""
newth = oldth + """
   <th data-k="se">Phiên (GA4)</th><th data-k="en">Tương tác</th><th data-k="ke">Chuyển đổi</th>"""
assert oldth in h
h = h.replace(oldth, newth, 1)

oldtd = """   '<td>'+(r.po!==null?('<span class="pill '+(r.po<=10?'t-ok':(r.po<=20?'t-warn':'t-bad'))+'">'+r.po.toFixed(1)+'</span>'):'<span style="color:#9CA3AF">—</span>')+'</td></tr>';"""
newtd = """   '<td>'+(r.po!==null?('<span class="pill '+(r.po<=10?'t-ok':(r.po<=20?'t-warn':'t-bad'))+'">'+r.po.toFixed(1)+'</span>'):'<span style="color:#9CA3AF">—</span>')+'</td>'+
   '<td>'+(r.se>0?r.se.toLocaleString("vi-VN"):'<span style="color:#9CA3AF">—</span>')+'</td>'+
   '<td>'+(r.en!==null?('<span class="pill '+(r.en>=30?'t-ok':(r.en>=10?'t-warn':'t-bad'))+'">'+r.en+'s</span>'):'<span style="color:#9CA3AF">—</span>')+'</td>'+
   '<td>'+(r.se>0?'<span class="pill t-bad">0</span>':'<span style="color:#9CA3AF">—</span>')+'</td></tr>';"""
assert oldtd in h
h = h.replace(oldtd, newtd, 1)

h = h.replace('po:"Vị trí TB",opp:"Điểm cơ hội"', 'po:"Vị trí TB",opp:"Điểm cơ hội",se:"Phiên GA4",en:"Tương tác",ke:"Chuyển đổi"')

# header chip
h = h.replace('<span class="chip">GA4: <b>không truy cập được</b></span>',
              '<span class="chip">GA4: <b>property Kvytech · 30/04 – 29/07/2026</b></span>')
h = h.replace('kvytechnology.com · Crawl Chrome + Google Search Console + Ahrefs · Quét toàn bộ sitemap và đối chiếu dữ liệu hiệu quả thật',
              'kvytechnology.com · Crawl Chrome + Google Search Console + GA4 + Ahrefs · Quét toàn bộ sitemap và đối chiếu dữ liệu hiệu quả thật')
h = h.replace('<title>KVY Technology — Kiểm toán SEO tổng hợp (Crawl + GSC + Ahrefs) · 31/07/2026</title>',
              '<title>KVY Technology — Kiểm toán SEO tổng hợp (Crawl + GSC + GA4 + Ahrefs) · 31/07/2026</title>')

# khối GA4
ga_block = u"""
<h2 class="sec">Hành vi người dùng — Google Analytics 4 (30/04 – 29/07/2026)</h2>
<div class="kpis">
 <div class="card kpi">
  <div class="lbl">Chuyển đổi ghi nhận</div><div class="val">0</div>
  <span class="tag t-bad">Không có key event nào</span>
  <div class="note">Trong 3 tháng, trên toàn bộ 460 landing page: <b>0 key event, tỷ lệ chuyển đổi 0%, doanh thu 0₫</b>.
  GA4 chưa được cấu hình bất kỳ chuyển đổi nào — KVY hiện <b>không thể đo được một lead nào</b> từ website.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Tổng số phiên</div><div class="val">7.003</div>
  <span class="tag t-info">5.957 người dùng</span>
  <div class="note">Trung bình ~78 phiên/ngày. So sánh: GSC ghi nhận 975 lượt nhấp tự nhiên, GA4 ghi nhận 1.600 phiên Organic Search
  (chênh lệch đến từ Bing và các máy tìm kiếm khác).</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Thời gian tương tác / phiên</div><div class="val">16<small>s</small></div>
  <span class="tag t-bad">Trung vị 7s</span>
  <div class="note">26/100 landing page hàng đầu có thời gian tương tác <b>đúng 0 giây</b>. Trang có tương tác tốt nhất là
  case study <code>/cerebro-ai-driven-crypto</code> với 1 phút 19 giây.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Người dùng mới</div><div class="val">99<small>,1%</small></div>
  <span class="tag t-bad">5.905 / 5.957</span>
  <div class="note">Gần như không có người quay lại. Kết hợp với tương tác 16 giây, đây là dấu hiệu điển hình của lưu lượng
  chất lượng thấp hoặc bot, không phải người đọc thật.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Phiên vào trang /contact</div><div class="val">47</div>
  <span class="tag t-bad">~0,5 phiên/ngày</span>
  <div class="note">Trang liên hệ nhận 47 phiên trong 3 tháng, tương tác 11 giây. Đây là toàn bộ phễu cuối của website.</div>
 </div>
</div>

<div class="two" style="margin-top:14px">
 <div class="card">
  <div style="font-size:13px;font-weight:700;margin-bottom:14px">Phiên theo kênh (GA4, 3 tháng)</div>
  <div id="chan"></div>
  <div style="font-size:11.5px;color:#6B7280;margin-top:14px;line-height:1.7">
   <b>Direct chiếm 61%</b> — tỷ lệ bất thường với một site B2B không chạy quảng cáo và không có thương hiệu tiêu dùng.
   Thông thường đây là dấu hiệu của bot, lưu lượng không gắn UTM, hoặc referral spam bị phân loại nhầm.
   Organic Search chỉ 1.600 phiên, Organic Social 181 phiên trong cả 3 tháng.
  </div>
 </div>
 <div class="card">
  <div style="font-size:13px;font-weight:700;margin-bottom:14px">Top landing page theo phiên (GA4)</div>
  <div id="galp"></div>
  <div style="font-size:11.5px;color:#6B7280;margin-top:14px;line-height:1.7">
   Trang chủ chiếm 25,8% tổng phiên. <code>(not set)</code> chiếm 333 phiên (4,8%) — đây là lỗ hổng đo lường,
   GA4 không xác định được landing page. Trong 100 landing page hàng đầu chỉ có
   <b>2 trang dịch vụ</b> (<code>/b2c-ecommerce-development-services</code> 15 phiên · 0 giây và
   <code>/d2c-ecommerce-development-services</code> 14 phiên · 3 giây).
  </div>
 </div>
</div>
"""
anchor = '<h2 class="sec">Ahrefs — hồ sơ liên kết, thứ hạng và độ hiện diện AI (31/07/2026)</h2>'
assert anchor in h
h = h.replace(anchor, ga_block + '\n' + anchor, 1)

# insight GA4 — đặt lên đầu
ga_ins = u"""
<div class="ins p1">
 <div class="k">P1 — chặn mọi việc còn lại · phát hiện nhờ GA4</div>
 <h4>GA4 ghi nhận 0 chuyển đổi trong 3 tháng vì chưa có key event nào được cấu hình</h4>
 <p>Trên toàn bộ 460 landing page, 7.003 phiên và 5.957 người dùng: <b>key event = 0,00 · tỷ lệ chuyển đổi phiên = 0% · doanh thu = 0₫</b>.
 Không phải website không có ai liên hệ — mà là <b>GA4 chưa được cài đặt để đo bất cứ điều gì</b>.
 Chính GA4 cũng đang gợi ý: "Capture 6 weekly page views on path /contact that could be tracked as generate_lead key events".</p>
 <p>Hệ quả: mọi việc SEO trong bản audit này — thêm H1, sửa title, dọn URL neo — đều <b>không thể chứng minh được hiệu quả kinh doanh</b>.
 Không có số liệu nào trả lời được câu "SEO mang về bao nhiêu lead tháng này".</p>
 <div class="fix"><b>Cách sửa (làm trước tiên, mất khoảng 1 buổi):</b> trong GA4 → Admin → Events, tạo key event cho
 sự kiện submit form liên hệ, click nút "Book a call", click email và số điện thoại, tải ebook.
 Đánh dấu chúng là Key event. Song song, gắn UTM cho mọi link outbound (LinkedIn, email, chữ ký, directory)
 để phần Direct 61% được phân loại đúng.</div>
</div>

<div class="ins p2">
 <div class="k">P2 — chất lượng lưu lượng</div>
 <h4>Tương tác 16 giây/phiên, 99,1% người dùng mới, Direct chiếm 61% — nhiều khả năng có lưu lượng rác</h4>
 <p>GA4 tự phát hiện: ngày 20/07/2026 phiên vào trang chủ tăng vọt lên 515 (dự báo 13), do
 <b>referral tăng từ 2 lên 504</b> và <b>500 phiên mới đến từ Seychelles</b>. Đây là dấu hiệu referral spam kinh điển.</p>
 <p>Trung vị thời gian tương tác của 100 landing page hàng đầu chỉ <b>7 giây</b>, trong đó 26 trang bằng <b>0 giây</b> —
 kể cả những trang quan trọng như <code>/methodology</code> (45 phiên · 0 giây) và
 <code>/b2c-ecommerce-development-services</code> (15 phiên · 0 giây).</p>
 <p>Nghĩa là con số 7.003 phiên đang bị thổi phồng. Lưu lượng người thật có ý định tìm hiểu dịch vụ thấp hơn nhiều so với vẻ ngoài.</p>
 <div class="fix"><b>Cách sửa:</b> bật bộ lọc lưu lượng nội bộ và lưu lượng nhà phát triển trong GA4,
 tạo segment loại trừ Seychelles và các nguồn referral lạ, rồi đọc lại số liệu 3 tháng.
 Đặt lại đường cơ sở (baseline) sau khi đã lọc — đừng lấy 7.003 phiên làm mốc so sánh cho các kỳ sau.</div>
</div>

<div class="ins p2">
 <div class="k">P2 — nội dung nào thật sự giữ chân người đọc</div>
 <h4>Case study giữ người đọc lâu gấp 5 lần blog, nhưng gần như không có ai vào</h4>
 <p><code>/cerebro-ai-driven-crypto</code> đạt <b>1 phút 19 giây</b> — cao nhất toàn site, gấp 5 lần mức trung bình 16 giây —
 nhưng chỉ có 15 phiên trong 3 tháng. Các bài blog có tương tác tốt cũng cùng nhóm chủ đề chuyên sâu:
 <code>disadvantages-of-medusa-js</code> 51 giây, <code>top-strapi-plugins</code> 47 giây,
 <code>agile-case-studies</code> 39 giây, <code>3-step-guide-for-singpass-integration</code> 35 giây.</p>
 <p>Ngược lại, nhóm bài viết chung chung về ecommerce theo quốc gia có lượt xem cao nhưng tương tác 1–9 giây.</p>
 <div class="fix"><b>Cách sửa:</b> đây là bằng chứng nên đầu tư vào case study và nội dung kỹ thuật sâu thay vì bài tổng quan.
 Trước mắt: liên kết nội bộ từ các bài blog đang có traffic về case study và trang dịch vụ tương ứng,
 và đưa case study lên điều hướng chính thay vì chôn trong <code>/showcases/</code>.</div>
</div>
"""
anchor2 = '<div class="ins p1">\n <div class="k">P1 — nghiêm trọng · phát hiện nhờ Search Console</div>'
assert anchor2 in h
h = h.replace(anchor2, ga_ins + '\n' + anchor2, 1)

# lộ trình: chèn bước đo lường lên trước
oldr = """ <p><b>0.</b> Tắt ID neo tự sinh của Elementor"""
newr = """ <p><b>0.</b> Cấu hình key event trong GA4 (submit form, book a call, click email/điện thoại, tải ebook) và gắn UTM cho link outbound. Không có bước này thì không đo được kết quả của 6 bước còn lại.</p>
 <p><b>0b.</b> Tắt ID neo tự sinh của Elementor"""
assert oldr in h
h = h.replace(oldr, newr, 1)

# JS biểu đồ GA4
js = u"""
var CHAN=[["Direct",4300,61.4,"#D64545"],["Organic Search",1600,22.8,"#1B9E5A"],["Referral",717,10.2,"#D98324"],
["Organic Social",181,2.6,"#0049FD"],["Unassigned",53,0.8,"#6B7280"],["AI Assistant / khác",152,2.2,"#8B5CF6"]];
document.getElementById("chan").innerHTML = CHAN.map(function(s){
 return '<div class="lg"><span class="sw" style="background:'+s[3]+'"></span><span style="flex:1">'+s[0]+'</span><b>'+s[1].toLocaleString("vi-VN")+'</b><span style="color:#6B7280;width:48px;text-align:right">'+s[2]+'%</span></div>'+
 '<div class="track" style="height:9px;margin-bottom:9px"><div class="fill" style="width:'+s[2]+'%;background:'+s[3]+'"></div></div>';
}).join("");

var LP=[]; for(var z=0;z<D.length;z++) if(D[z].se>0) LP.push(D[z]);
for(var a2=0;a2<LP.length;a2++) for(var b2=a2+1;b2<LP.length;b2++) if(LP[b2].se>LP[a2].se){var t2=LP[a2];LP[a2]=LP[b2];LP[b2]=t2;}
var mxs = LP.length?LP[0].se:1;
document.getElementById("galp").innerHTML = LP.slice(0,12).map(function(r){
 var c = r.en>=30?"#1B9E5A":(r.en>=10?"#D98324":"#D64545");
 return '<div class="ttfbrow" style="grid-template-columns:210px 1fr 78px"><div class="u" title="'+r.p+'">'+r.p+'</div>'+
 '<div><div class="b" style="width:'+(r.se/mxs*100).toFixed(1)+'%;background:'+c+'"></div></div>'+
 '<div class="v">'+r.se+' · '+r.en+'s</div></div>';
}).join("");
"""
h = h.replace('draw();\n</script>', js + '\ndraw();\n</script>', 1)

# footer
h = h.replace(u'GA4 không đưa vào được vì tài khoản Google đang đăng nhập chỉ có property TechnoWindow, không có property của KVY.',
 u'''GA4 property "Kvytech" (tài khoản KVY TECH 2025, ID a269209106p377750984), khoảng 30/04–29/07/2026, báo cáo Engagement → Landing page, 100 landing page hàng đầu trên tổng 460.
 Cột Phiên/Tương tác chỉ có ở 94 trang khớp được giữa GA4 và sitemap; cột Chuyển đổi hiển thị 0 vì GA4 chưa cấu hình key event nào.''')

io.open('kvy-seo-audit-dashboard-v3.html','w',encoding='utf-8').write(h)
print("OK", len(h))
