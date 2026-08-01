# -*- coding: utf-8 -*-
import re, io

h = io.open('kvy-seo-audit-dashboard.html', encoding='utf-8').read()
raw = io.open('kvy-merged-data.csv', encoding='utf-8').read().strip()

# ---------- 1. thay dữ liệu ----------
h = re.sub(r'var RAW = `[\s\S]*?`;', 'var RAW = `' + raw + '`;', h, count=1)

# ---------- 2. parser mới (thêm clicks / impressions / position) ----------
old_parse = """  return {p:p,g:+a[1],s:200,t:+a[2],w:+a[3],ld:+a[4],f:+a[5],il:+a[6],im:+a[7],na:+a[8],h1:+a[9],tl:+a[10],dl:+a[11],kb:+a[12]};"""
new_parse = """  var cl=+a[13], ip=+a[14], po=a[15]===""?null:+a[15];
  var ctr = ip>0 ? (cl/ip*100) : null;
  var opp = 0;
  if(ip>=500 && po!==null && po>=6 && po<=35 && cl<=10) opp = ip*(1/Math.max(po,6));
  return {p:p,g:+a[1],s:200,t:+a[2],w:+a[3],ld:+a[4],f:+a[5],il:+a[6],im:+a[7],na:+a[8],h1:+a[9],tl:+a[10],dl:+a[11],kb:+a[12],cl:cl,ip:ip,po:po,ctr:ctr,opp:opp};"""
assert old_parse in h
h = h.replace(old_parse, new_parse, 1)

# ---------- 3. tiêu đề bảng: thêm cột ----------
old_th = """   <th data-k="im">Ảnh</th><th data-k="na">Thiếu alt</th><th data-k="il">Link nội bộ</th>"""
new_th = """   <th data-k="im">Ảnh</th><th data-k="na">Thiếu alt</th><th data-k="il">Link nội bộ</th>
   <th data-k="cl">Clicks (GSC)</th><th data-k="ip">Impressions</th><th data-k="ctr">CTR</th><th data-k="po">Vị trí TB</th>"""
assert old_th in h
h = h.replace(old_th, new_th, 1)

# ---------- 4. ô dữ liệu: thêm 4 cột ----------
old_td = """   '<td>'+r.il+'</td></tr>';"""
new_td = """   '<td>'+r.il+'</td>'+
   '<td>'+(r.ip>0?('<span class="pill '+(r.cl>=10?'t-ok':(r.cl>0?'t-warn':'t-bad'))+'">'+r.cl+'</span>'):'<span style="color:#9CA3AF">—</span>')+'</td>'+
   '<td>'+(r.ip>0?r.ip.toLocaleString("vi-VN"):'<span style="color:#9CA3AF">—</span>')+'</td>'+
   '<td>'+(r.ip>0?('<span class="pill '+(r.ctr>=1?'t-ok':(r.ctr>=0.2?'t-warn':'t-bad'))+'">'+r.ctr.toFixed(2)+'%</span>'):'<span style="color:#9CA3AF">—</span>')+'</td>'+
   '<td>'+(r.po!==null?('<span class="pill '+(r.po<=10?'t-ok':(r.po<=20?'t-warn':'t-bad'))+'">'+r.po.toFixed(1)+'</span>'):'<span style="color:#9CA3AF">—</span>')+'</td></tr>';"""
assert old_td in h
h = h.replace(old_td, new_td, 1)

# tên cột trong dòng chú thích
h = h.replace('il:"Link nội bộ",s:"Status"', 'il:"Link nội bộ",s:"Status",cl:"Clicks",ip:"Impressions",ctr:"CTR",po:"Vị trí TB",opp:"Điểm cơ hội"')

# ---------- 5. header: nguồn dữ liệu ----------
h = h.replace(
 '<div class="sub">kvytechnology.com · Crawl trực tiếp qua Chrome (same-origin fetch, TTFB đo thật) · Quét toàn bộ sitemap</div>',
 '<div class="sub">kvytechnology.com · Crawl Chrome + Google Search Console + Ahrefs · Quét toàn bộ sitemap và đối chiếu dữ liệu hiệu quả thật</div>')
h = h.replace(
 '<span class="chip">Phương pháp: <b>Chrome fetch · TTFB đo riêng ở concurrency 4</b></span>',
 '<span class="chip">GSC: <b>30/04 – 29/07/2026 (3 tháng)</b></span>\n  <span class="chip">Ahrefs: <b>snapshot 31/07/2026</b></span>\n  <span class="chip">GA4: <b>không truy cập được</b></span>')

# ---------- 6. cập nhật điểm & KPI ----------
h = h.replace('<div class="val">80<small>/100</small></div>', '<div class="val">64<small>/100</small></div>')
h = h.replace('<span class="tag t-warn">Tốt — còn 2 lỗi lớn</span>', '<span class="tag t-bad">Cần can thiệp</span>')
h = h.replace(
 '<div class="note">Kéo điểm xuống chủ yếu là On-page (60/100): 61 trang không có H1 và 342 trang sai thứ tự heading. Nền kỹ thuật rất vững.</div>',
 '<div class="note">Bản v1 chấm 80 khi chỉ có dữ liệu kỹ thuật. Sau khi ghép GSC và Ahrefs, điểm giảm còn 64: site sạch về kỹ thuật nhưng gần như không chuyển được hiển thị thành click.</div>')
h = h.replace(
 '[["Crawlability",96,"#1B9E5A"],["Hiệu năng / TTFB",72,"#D98324"],["Structured Data / AEO",85,"#1B9E5A"],\n["On-page / Meta",60,"#D64545"],["Nội dung &amp; ảnh",77,"#D98324"]]',
 '[["Crawlability &amp; Index",62,"#D64545"],["Hiệu năng / TTFB",72,"#D98324"],["Structured Data / AEO",70,"#D98324"],\n["On-page / CTR",48,"#D64545"],["Nội dung &amp; ảnh",65,"#D98324"]]')
h = h.replace(
 'Trọng số: Crawlability 25% · Hiệu năng 25% · Schema/AEO 20% · On-page 15% · Nội dung 15% → tổng <b>80/100</b>.',
 'Trọng số: Crawlability 25% · Hiệu năng 25% · Schema/AEO 20% · On-page 15% · Nội dung 15% → tổng <b>64/100</b>.')
h = h.replace(
 """   Crawlability gần như hoàn hảo (365/365 status 200, robots.txt hợp lệ, sitemap khai báo đúng, URL không tồn tại trả đúng mã 404)
   — chỉ trừ điểm ở 7 trang canonical lệch URL. On-page là điểm yếu duy nhất và đều bắt nguồn từ template, không phải từ nội dung.""",
 """   Crawlability tụt từ 96 xuống 62 vì GSC cho thấy chỉ <b>288 trang được index</b> trong khi <b>392 trang không được index</b>
   — con số mà bản crawl kỹ thuật không nhìn thấy được. On-page tụt còn 48 vì CTR toàn site chỉ 0,2%: site có hiển thị nhưng không có click.""")

# ---------- 7. chèn khối GSC + Ahrefs ngay trước mục "Vấn đề" ----------
block = u"""
<h2 class="sec">Hiệu quả thật — Google Search Console (30/04 – 29/07/2026)</h2>
<div class="kpis">
 <div class="card kpi">
  <div class="lbl">Tổng lượt nhấp</div><div class="val">975</div>
  <span class="tag t-bad">~325 click/tháng</span>
  <div class="note">Trên toàn bộ site trong 3 tháng. Đây là toàn bộ traffic tự nhiên mà 365 trang và 292 bài blog mang về.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Tổng lượt hiển thị</div><div class="val">592<small>N</small></div>
  <span class="tag t-info">Hiển thị rất tốt</span>
  <div class="note">592.000 lượt hiển thị. Vấn đề không nằm ở việc Google không thấy KVY — Google thấy rất nhiều.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">CTR trung bình</div><div class="val">0,2<small>%</small></div>
  <span class="tag t-bad">Thấp nghiêm trọng</span>
  <div class="note">Cứ 500 lần xuất hiện trên Google mới có 1 người bấm vào. Đây là chỉ số tệ nhất của toàn bộ bản audit.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Vị trí trung bình</div><div class="val">26,1</div>
  <span class="tag t-bad">Trang 3 kết quả</span>
  <div class="note">Phần lớn hiển thị đến từ vị trí 11–30, nơi CTR gần bằng 0. 624/763 URL có hiển thị nhưng <b>0 click</b>.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Trang được index</div><div class="val">288<small>/680</small></div>
  <span class="tag t-bad">392 trang không index</span>
  <div class="note">Sitemap khai báo 365 URL nhưng Google chỉ index 288. Số liệu cập nhật 24/07/2026.</div>
 </div>
</div>

<h2 class="sec">Ahrefs — hồ sơ liên kết, thứ hạng và độ hiện diện AI (31/07/2026)</h2>
<div class="kpis">
 <div class="card kpi">
  <div class="lbl">Domain Rating</div><div class="val">27</div>
  <span class="tag t-warn">UR 6</span>
  <div class="note">922 backlink từ 562 referring domain (+148 tháng qua). Nền link đang lên đều — đây là tài sản thật.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Từ khoá tự nhiên</div><div class="val">62</div>
  <span class="tag t-bad">−27 tháng qua</span>
  <div class="note">Chỉ 62 từ khoá có thứ hạng, Top 3 còn 24 (−13). Xu hướng giảm rõ rệt.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Traffic tự nhiên / tháng</div><div class="val">162</div>
  <span class="tag t-bad">−21 · giá trị $350</span>
  <div class="note">Chỉ <b>40/365 trang</b> có traffic tự nhiên, tổng 172 lượt. 325 trang còn lại bằng 0.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Hiện diện AI Overviews</div><div class="val">27</div>
  <span class="tag t-warn">−7 · 20 trang</span>
  <div class="note">AI Mode 43 phản hồi / 29 trang (+7). Gemini 1, Copilot 1, Perplexity 0.</div>
 </div>
 <div class="card kpi">
  <div class="lbl">Hiện diện ChatGPT</div><div class="val">0</div>
  <span class="tag t-bad">0 trang được trích dẫn</span>
  <div class="note">Với một công ty định vị AI-first, đây là khoảng trống lớn nhất về AEO.</div>
 </div>
</div>

<div class="two" style="margin-top:14px">
 <div class="card">
  <div style="font-size:13px;font-weight:700;margin-bottom:14px">Vì sao 392 trang không được index</div>
  <div id="idx"></div>
  <div style="font-size:11.5px;color:#6B7280;margin-top:14px;line-height:1.7">
   <b>246 trang "đã thu thập dữ liệu – hiện chưa được index"</b> là nhóm lớn nhất và cũng là tín hiệu chất lượng:
   Google đã đọc nhưng quyết định không đưa vào chỉ mục. <b>78 trang lỗi 404</b> đang được Google chủ động thử lại —
   nghĩa là còn link trỏ tới chúng từ đâu đó. 30 trang redirect và 12 trang canonical thay thế là bình thường.
  </div>
 </div>
 <div class="card">
  <div style="font-size:13px;font-weight:700;margin-bottom:14px">Traffic tự nhiên theo quốc gia (Ahrefs)</div>
  <div id="geo"></div>
  <div style="font-size:11.5px;color:#6B7280;margin-top:14px;line-height:1.7">
   KVY định vị mạnh cho thị trường <b>Singapore</b> nhưng Singapore chỉ chiếm <b>3,7%</b> traffic tự nhiên — 6 lượt/tháng.
   Gần 79% traffic đến từ Mỹ, chủ yếu qua các bài blog kỹ thuật chung chung (agile, strapi, medusa) chứ không phải nội dung B2B Singapore.
  </div>
 </div>
</div>

<h2 class="sec">30 trang có cơ hội cao nhất — nhiều hiển thị, vị trí 6–35, gần như không có click</h2>
<div class="card">
 <div class="tblbox" style="max-height:520px"><table>
  <thead><tr><th>#</th><th>URL</th><th>Impressions</th><th>Clicks</th><th>CTR</th><th>Vị trí TB</th><th>Title</th><th>Meta desc</th><th>H1</th><th>Số từ</th></tr></thead>
  <tbody id="opptb"></tbody>
 </table></div>
 <div style="font-size:11.5px;color:#6B7280;margin-top:12px;line-height:1.7">
  Đây là danh sách việc cần làm thực tế. Các trang này Google đã cho hiển thị hàng nghìn tới hàng chục nghìn lần,
  đứng ở vị trí 6–35 — tức chỉ cần đẩy lên vài bậc và viết lại title/description là có click ngay,
  không cần viết bài mới. Sắp theo <i>impressions ÷ vị trí</i>.
 </div>
</div>
"""
anchor = '<h2 class="sec">Vấn đề &amp; thứ tự ưu tiên</h2>'
assert anchor in h
h = h.replace(anchor, block + '\n' + anchor, 1)

# ---------- 8. các insight mới, chèn lên đầu danh sách vấn đề ----------
newins = u"""
<div class="ins p1">
 <div class="k">P1 — nghiêm trọng · phát hiện nhờ Search Console</div>
 <h4>592.000 lượt hiển thị nhưng chỉ 975 click — CTR 0,2%</h4>
 <p>Trong 3 tháng, KVY xuất hiện trên Google gần 600 nghìn lần và nhận về 975 lượt nhấp.
 <b>624 trên 763 URL có hiển thị nhưng không nhận được một click nào.</b>
 Vị trí trung bình 26,1 — tức phần lớn hiển thị rơi vào trang 2 và trang 3, nơi CTR gần bằng 0.</p>
 <p>Đây mới là vấn đề lớn nhất của site, và bản audit kỹ thuật thuần tuý không thể nhìn thấy.
 Nền kỹ thuật sạch (365/365 trả 200, TTFB 806ms, 355 trang có schema) nhưng không chuyển được thành lưu lượng.</p>
 <div class="fix"><b>Cách sửa:</b> tập trung vào bảng "30 trang cơ hội" phía trên thay vì viết bài mới.
 Viết lại title và meta description theo đúng truy vấn người dùng gõ, bổ sung nội dung để đẩy từ vị trí 15–25 lên top 10.
 Chỉ cần 10 trang đầu bảng lên được top 10 là traffic tăng gấp nhiều lần.</div>
</div>

<div class="ins p1">
 <div class="k">P1 — nghiêm trọng · lãng phí hiển thị</div>
 <h4>427 URL neo (#anchor) của Elementor ngốn 145.203 lượt hiển thị và mang về đúng 0 click</h4>
 <p>Mục lục tự động của Elementor sinh ra các URL dạng
 <code>/blog/software/software-scalability/#elementor-toc__heading-anchor-0</code> và
 <code>/blog/software/agile-case-studies/#Agile-Case-study-15</code>.
 Google đang xếp hạng chúng như kết quả riêng biệt. Riêng 3 biến thể neo của bài <i>software-scalability</i>
 chiếm 96.930 lượt hiển thị ở vị trí 9,5 — và <b>0 click</b>.</p>
 <p>Tổng cộng 427 URL neo, 145.203 lượt hiển thị (19,4% toàn site), 0 click.
 Chúng đang cạnh tranh trực tiếp với chính trang gốc và làm loãng tín hiệu xếp hạng.</p>
 <div class="fix"><b>Cách sửa:</b> tắt tính năng "Add anchor to headings" hoặc bỏ ID neo tự sinh trong widget Table of Contents của Elementor;
 nếu vẫn muốn giữ mục lục thì dùng JavaScript scroll thay vì đổi URL. Đây là một cài đặt duy nhất, sửa xong là 427 URL rác biến mất.</div>
</div>

<div class="ins p1">
 <div class="k">P1 — nghiêm trọng · toàn bộ phễu thương mại</div>
 <h4>37 trang dịch vụ mang về đúng 6 click trong 3 tháng</h4>
 <p>Toàn bộ nhóm landing page dịch vụ — nơi đáng lẽ phải tạo ra lead — chỉ có <b>5.644 lượt hiển thị và 6 lượt nhấp</b> trong 3 tháng.
 Trong bảng Top pages của Ahrefs, <b>không một trang dịch vụ nào lọt vào 25 trang có traffic cao nhất</b>; tất cả đều là bài blog.</p>
 <p>Nhóm 61 trang thiếu H1 (chủ yếu là trang dịch vụ) tổng cộng chỉ 29 click / 10.564 hiển thị.
 Việc thiếu H1 và việc các trang này vô hình trên Google là hai mặt của cùng một vấn đề.</p>
 <div class="fix"><b>Cách sửa:</b> ngoài việc thêm H1, cần xử lý gốc rễ: các trang dịch vụ hiện viết theo ngôn ngữ giới thiệu năng lực,
 không nhắm truy vấn thương mại cụ thể. Chọn 5 trang ưu tiên, gắn mỗi trang vào một cụm từ khoá có nhu cầu thật,
 và liên kết nội bộ từ các bài blog đang có hiển thị cao về đúng trang dịch vụ tương ứng.</div>
</div>

<div class="ins p2">
 <div class="k">P2 — cần xử lý · chất lượng chỉ mục</div>
 <h4>246 trang bị Google "đã thu thập nhưng không index" + 78 trang lỗi 404</h4>
 <p>Chỉ <b>288 trang được index</b> trong khi sitemap khai báo 365 URL. Google đã đọc 246 trang rồi quyết định không đưa vào chỉ mục —
 đây là đánh giá chất lượng, không phải lỗi kỹ thuật. Thường gặp ở trang mỏng, trùng lặp hoặc không có nhu cầu tìm kiếm.</p>
 <p><b>78 trang trả lỗi 404</b> vẫn đang được Google thử lại, nghĩa là còn link trỏ tới chúng.
 Ngoài ra có 9 trang soft 404, 5 lỗi chuyển hướng và 2 trang trùng lặp chưa chọn canonical.</p>
 <p>Bản crawl kỹ thuật cho kết quả 365/365 trả 200 — vì nó chỉ đi theo sitemap. 78 URL 404 kia nằm ngoài sitemap,
 đến từ link cũ, link nội bộ hỏng hoặc backlink trỏ sai.</p>
 <div class="fix"><b>Cách sửa:</b> tải danh sách 78 URL 404 từ GSC, đối chiếu với báo cáo Backlinks của Ahrefs để tìm URL nào còn nhận link,
 rồi 301 về trang tương đương. Với 246 trang crawled-not-indexed: gộp hoặc noindex các trang mỏng, đặc biệt là 19 trang taxonomy dưới 300 từ.</div>
</div>

<div class="ins p2">
 <div class="k">P2 — cần xử lý · trùng lặp</div>
 <h4>Bài viết được đăng trùng ở hai chuyên mục khác nhau</h4>
 <p>GSC ghi nhận cả <code>/blog/ai/generative-ai-in-the-integration/</code> và
 <code>/blog/technologies/generative-ai-in-the-integration/</code>, tương tự với
 <code>ai-consulting-services-for-modern-enterprises</code> ở cả <code>/blog/ai/</code> và <code>/blog/technologies/</code>.
 Hai phiên bản cùng nội dung tự cạnh tranh nhau.</p>
 <p>Cộng thêm bản sao trang chủ <code>/home-2/</code> đã nêu ở phần dưới, đây là dấu hiệu cấu trúc chuyên mục chưa được kiểm soát.</p>
 <div class="fix"><b>Cách sửa:</b> chọn một URL chính cho mỗi bài, 301 bản còn lại về đó. Rà lại toàn bộ bài nằm ở nhiều hơn một chuyên mục.</div>
</div>

<div class="ins p2">
 <div class="k">P2 — cần xử lý · AEO</div>
 <h4>ChatGPT trích dẫn KVY 0 lần; AI Overviews đang giảm</h4>
 <p>Theo Brand Radar của Ahrefs: ChatGPT <b>0 phản hồi, 0 trang</b>; Perplexity 0; Gemini 1; Copilot 1.
 Google AI Overviews có 27 lần nhắc trên 20 trang nhưng <b>giảm 7</b> so với tháng trước.
 Điểm sáng duy nhất là Google AI Mode: 43 phản hồi trên 29 trang, tăng 7.</p>
 <p>Với một công ty tự định vị là đối tác AI production-grade, gần như vô hình trong chính các công cụ AI là một mâu thuẫn đáng chú ý.
 Nguyên nhân kỹ thuật đã thấy trong bản audit: 61 trang không H1, thứ tự heading vỡ trên 342 trang, FAQPage mới phủ 33/365 trang,
 3 trang usecase AI dài trên 5.400 từ nhưng không có schema nào.</p>
 <div class="fix"><b>Cách sửa:</b> ưu tiên đúng ba việc đã nêu — thêm H1, sửa heading, gắn schema cho usecase —
 rồi mở rộng FAQPage sang toàn bộ trang dịch vụ và cụm bài AI. Đây là điều kiện cần để nội dung được trích dẫn lại.</div>
</div>
"""
anchor2 = '<div class="ins p1">\n <div class="k">P1 — nghiêm trọng · ảnh hưởng trực tiếp tới trang mang lead</div>'
assert anchor2 in h
h = h.replace(anchor2, newins + '\n' + anchor2, 1)

# ---------- 9. cập nhật lộ trình ----------
old_road = """ <p><b>1.</b> Thêm H1 cho 61 trang thiếu, bắt đầu từ 37 landing page dịch vụ. Tác động cao nhất, công sức thấp nhất vì sửa ở template.</p>"""
new_road = """ <p><b>0.</b> Tắt ID neo tự sinh của Elementor Table of Contents — dọn 427 URL rác đang ngốn 145.203 lượt hiển thị mà không mang về click nào. Một cài đặt, hiệu quả tức thì.</p>
 <p><b>1.</b> Viết lại title và meta description cho 30 trang trong bảng "Cơ hội" — nhóm đang có hiển thị lớn ở vị trí 6–35. Đây là nguồn traffic nhanh nhất, không cần viết bài mới.</p>
 <p><b>2.</b> Thêm H1 cho 61 trang thiếu, bắt đầu từ 37 landing page dịch vụ (hiện chỉ mang về 6 click / 3 tháng).</p>"""
assert old_road in h
h = h.replace(old_road, new_road, 1)
h = h.replace(' <p><b>2.</b> Đổi 81 thẻ H6 trong mega-menu thành span. Sửa một lần, 342 trang hết lỗi thứ tự heading.</p>',
              ' <p><b>3.</b> Đổi 81 thẻ H6 trong mega-menu thành span. Sửa một lần, 342 trang hết lỗi thứ tự heading.</p>')
h = h.replace(' <p><b>3.</b> Dọn 3 trang rác:', ' <p><b>4.</b> Dọn 78 URL lỗi 404 (301 về trang tương đương) và 3 trang rác:')
h = h.replace(' <p><b>4.</b> Bổ sung alt cho 1.776 ảnh', ' <p><b>5.</b> Bổ sung alt cho 1.776 ảnh')
h = h.replace(' <p><b>5.</b> Gắn schema cho 10 trang usecase', ' <p><b>6.</b> Gắn schema cho 10 trang usecase')
h = h.replace('<h4>Việc cần làm sau bản audit ngày 31/07</h4>', '<h4>Việc cần làm — đã xếp lại theo dữ liệu hiệu quả thật</h4>')

# ---------- 10. JS cho 3 biểu đồ mới ----------
js = u"""
var IDX=[["Đã thu thập – chưa index",246,"#D64545"],["Không tìm thấy (404)",78,"#D64545"],
["Trang có lệnh chuyển hướng",30,"#D98324"],["Canonical thay thế hợp lệ",12,"#6B7280"],
["Lỗi 404 mềm",9,"#D98324"],["Bị loại trừ bởi noindex",8,"#6B7280"],
["Lỗi chuyển hướng",5,"#D98324"],["Khác (4xx, trùng lặp, robots)",4,"#6B7280"]];
document.getElementById("idx").innerHTML = IDX.map(function(s){
 return '<div class="barrow" style="grid-template-columns:190px 1fr 40px"><div class="n" style="font-size:12px">'+s[0]+'</div><div class="track"><div class="fill" style="width:'+(s[1]/246*100).toFixed(1)+'%;background:'+s[2]+'"></div></div><div class="s" style="color:'+s[2]+'">'+s[1]+'</div></div>';
}).join("");

var GEO=[["Hoa Kỳ",127,78.9,"#0049FD"],["Ấn Độ",11,6.8,"#4C7DFF"],["Úc",8,5.0,"#7FA3FF"],
["Singapore",6,3.7,"#D64545"],["Nga",5,3.1,"#B9C7E8"],["Khác",5,2.5,"#D5DCEB"]];
document.getElementById("geo").innerHTML = GEO.map(function(s){
 return '<div class="lg"><span class="sw" style="background:'+s[3]+'"></span><span style="flex:1">'+s[0]+(s[0]==="Singapore"?' <b style="color:#D64545">← thị trường mục tiêu</b>':'')+'</span><b>'+s[1]+'</b><span style="color:#6B7280;width:48px;text-align:right">'+s[2]+'%</span></div>'+
 '<div class="track" style="height:9px;margin-bottom:9px"><div class="fill" style="width:'+s[2]+'%;background:'+s[3]+'"></div></div>';
}).join("");

var OPP=[]; for(var q=0;q<D.length;q++) if(D[q].opp>0) OPP.push(D[q]);
for(var a1=0;a1<OPP.length;a1++) for(var b1=a1+1;b1<OPP.length;b1++) if(OPP[b1].opp>OPP[a1].opp){var tmp=OPP[a1];OPP[a1]=OPP[b1];OPP[b1]=tmp;}
document.getElementById("opptb").innerHTML = OPP.slice(0,30).map(function(r,i){
 var tlc=(r.tl>=30&&r.tl<=65)?"t-ok":"t-warn";
 var dlc=r.dl===0?"t-bad":((r.dl>=120&&r.dl<=165)?"t-ok":"t-warn");
 var h1c=r.h1===1?"t-ok":"t-bad";
 return '<tr><td style="color:#9CA3AF">'+(i+1)+'</td><td class="u" title="'+r.p+'">'+r.p+'</td>'+
  '<td><b>'+r.ip.toLocaleString("vi-VN")+'</b></td>'+
  '<td><span class="pill '+(r.cl>0?"t-warn":"t-bad")+'">'+r.cl+'</span></td>'+
  '<td><span class="pill t-bad">'+r.ctr.toFixed(2)+'%</span></td>'+
  '<td><span class="pill '+(r.po<=10?"t-ok":(r.po<=20?"t-warn":"t-bad"))+'">'+r.po.toFixed(1)+'</span></td>'+
  '<td><span class="pill '+tlc+'">'+r.tl+'</span></td>'+
  '<td><span class="pill '+dlc+'">'+r.dl+'</span></td>'+
  '<td><span class="pill '+h1c+'">'+r.h1+'</span></td>'+
  '<td>'+r.w.toLocaleString("vi-VN")+'</td></tr>';
}).join("");
"""
h = h.replace('draw();\n</script>', js + '\ndraw();\n</script>', 1)

# ---------- 11. footer ----------
h = h.replace('Điểm sức khoẻ là thang chấm nội bộ để so sánh giữa các kỳ audit, không phải chỉ số chính thức của Google.',
 u'''<b>Nguồn dữ liệu hiệu quả:</b> Google Search Console (property https://kvytechnology.com/, khoảng 30/04–29/07/2026, báo cáo Hiệu suất theo Trang và báo cáo Lập chỉ mục trang cập nhật 24/07/2026)
 và Ahrefs Site Explorer (snapshot 31/07/2026, chế độ Subdomains). GA4 không đưa vào được vì tài khoản Google đang đăng nhập chỉ có property TechnoWindow, không có property của KVY.
 Cột Clicks/Impressions/CTR/Vị trí chỉ có ở các trang đạt tối thiểu 50 lượt hiển thị trong kỳ (257/365 trang); dấu — nghĩa là dưới ngưỡng đó.
 Tổng hiển thị theo cấp trang lớn hơn tổng của toàn site vì Search Console phân bổ hiển thị khác nhau giữa hai cấp báo cáo; các con số tổng lấy theo báo cáo tổng của GSC.
 Điểm sức khoẻ là thang chấm nội bộ để so sánh giữa các kỳ audit, không phải chỉ số chính thức của Google.''')

h = h.replace('<title>KVY Technology — Kiểm toán SEO kỹ thuật · 31/07/2026</title>',
              '<title>KVY Technology — Kiểm toán SEO tổng hợp (Crawl + GSC + Ahrefs) · 31/07/2026</title>')
h = h.replace('<h1>KVY Technology — Kiểm toán SEO kỹ thuật</h1>',
              '<h1>KVY Technology — Kiểm toán SEO tổng hợp</h1>')

io.open('kvy-seo-audit-dashboard-v2.html','w',encoding='utf-8').write(h)
print("OK", len(h))
