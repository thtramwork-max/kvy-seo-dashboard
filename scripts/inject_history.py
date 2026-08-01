# -*- coding: utf-8 -*-
"""Chèn khối 'Xu hướng theo ngày' vào index.html từ history/history.csv.
Chạy được nhiều lần: lần sau sẽ thay thế khối cũ chứ không nhân đôi."""
import io, os, re, csv, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX  = os.path.join(ROOT, 'index.html')
HIST = os.path.join(ROOT, 'history', 'history.csv')

START = '<!--HISTORY_START-->'
END   = '<!--HISTORY_END-->'

rows = list(csv.DictReader(io.open(HIST, encoding='utf-8')))
rows = rows[-60:]                       # giữ 60 ngày gần nhất cho biểu đồ
last = rows[-1] if rows else {}

def num(r, k):
    try: return float(r.get(k) or 0)
    except: return 0.0

METRICS = [
    ('gsc_clicks',        'Lượt nhấp GSC',        'up'),
    ('gsc_impressions',   'Lượt hiển thị GSC',    'up'),
    ('gsc_ctr',           'CTR (%)',              'up'),
    ('gsc_avg_position',  'Vị trí trung bình',    'down'),
    ('pages_indexed',     'Trang được index',     'up'),
    ('pages_not_indexed', 'Trang không index',    'down'),
    ('ga4_sessions',      'Phiên GA4',            'up'),
    ('ga4_key_events',    'Chuyển đổi GA4',       'up'),
    ('ga4_engagement_sec','Tương tác (giây)',     'up'),
    ('pages_no_h1',       'Trang thiếu H1',       'down'),
    ('imgs_missing_alt',  'Ảnh thiếu alt',        'down'),
    ('ttfb_median',       'TTFB trung vị (ms)',   'down'),
    ('ahrefs_dr',         'Domain Rating',        'up'),
    ('ahrefs_ref_domains','Referring domains',    'up'),
    ('ahrefs_org_keywords','Từ khoá tự nhiên',    'up'),
    ('ahrefs_org_traffic','Traffic Ahrefs/tháng', 'up'),
    ('health_score',      'Điểm sức khoẻ',        'up'),
]

data = {'dates': [r['date'] for r in rows]}
for k, _, _ in METRICS:
    data[k] = [num(r, k) for r in rows]

block = START + u'''
<h2 class="sec">Xu hướng theo ngày — cập nhật tự động 7:00 sáng</h2>
<div class="card">
 <div id="trendwrap"></div>
 <div style="font-size:11.5px;color:#6B7280;margin-top:14px;line-height:1.7">
  Mỗi dòng là một chỉ số theo thời gian, lấy từ <code>history/history.csv</code>. Mũi tên so sánh với lần đo trước.
  Xanh nghĩa là đi đúng hướng (với các chỉ số như "Trang thiếu H1" hay "Vị trí trung bình" thì giảm mới là tốt).
  Biểu đồ chỉ có ý nghĩa sau vài ngày tích luỹ dữ liệu.
 </div>
</div>
<script>
var HIST = ''' + json.dumps(data, ensure_ascii=False) + u''';
var HMETA = ''' + json.dumps([[k, n, d] for k, n, d in METRICS], ensure_ascii=False) + u''';
(function(){
 var w = document.getElementById('trendwrap'); if(!w) return;
 var n = HIST.dates.length;
 var html = '<table style="font-size:12.5px"><thead><tr><th style="cursor:default">Chỉ số</th>'+
   '<th style="cursor:default">Hiện tại</th><th style="cursor:default">Thay đổi</th>'+
   '<th style="cursor:default">'+n+' lần đo gần nhất</th></tr></thead><tbody>';
 HMETA.forEach(function(m){
  var k=m[0], name=m[1], good=m[2];
  var v=HIST[k]||[]; if(!v.length) return;
  var cur=v[v.length-1], prev=v.length>1?v[v.length-2]:null;
  var deltaTxt='<span style="color:#9CA3AF">—</span>';
  if(prev!==null){
   var d=cur-prev;
   if(d===0){ deltaTxt='<span style="color:#9CA3AF">không đổi</span>'; }
   else{
    var better = good==='up' ? d>0 : d<0;
    var sign = d>0?'+':'';
    deltaTxt='<span class="pill '+(better?'t-ok':'t-bad')+'">'+sign+(Math.round(d*100)/100)+'</span>';
   }
  }
  var mx=Math.max.apply(null,v), mn=Math.min.apply(null,v);
  var span=(mx-mn)||1;
  var spark=v.map(function(x){
   var hgt=Math.max(2, Math.round((x-mn)/span*22)+2);
   return '<span title="'+x+'" style="display:inline-block;width:6px;height:'+hgt+'px;background:#0049FD;opacity:.75;margin-right:2px;vertical-align:bottom;border-radius:1px"></span>';
  }).join('');
  html += '<tr><td>'+name+'</td><td><b>'+cur.toLocaleString('vi-VN')+'</b></td><td>'+deltaTxt+'</td>'+
          '<td style="min-width:200px">'+spark+'</td></tr>';
 });
 html += '</tbody></table>';
 w.innerHTML = html;
})();
</script>
''' + END

src = io.open(IDX, encoding='utf-8').read()

if START in src and END in src:
    src = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda m: block, src, count=1)
else:
    anchor = '<h2 class="sec">Tổng quan sức khỏe</h2>'
    assert anchor in src, 'khong tim thay diem chen'
    src = src.replace(anchor, block + '\n\n' + anchor, 1)

# cập nhật chip ngày cập nhật
today = last.get('date') or datetime.date.today().isoformat()
d = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%d/%m/%Y')
src = re.sub(r'<span class="chip blue">Ngày crawl: <b>[^<]*</b></span>',
             '<span class="chip blue">Cập nhật: <b>' + d + '</b></span>', src, count=1)

io.open(IDX, 'w', encoding='utf-8').write(src)
print('injected history, %d ngay, file %d bytes' % (len(rows), len(src)))
