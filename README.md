# KVY Technology — SEO Dashboard

Dashboard kiểm toán SEO tổng hợp cho [kvytechnology.com](https://kvytechnology.com), cập nhật tự động mỗi ngày lúc 7:00.

**Xem dashboard:** mở `index.html` hoặc truy cập GitHub Pages của repo này.

## Nguồn dữ liệu

| Nguồn | Nội dung | Tần suất thay đổi |
|---|---|---|
| Crawl trực tiếp qua Chrome | TTFB, HTTP status, số từ, H1, heading, JSON-LD, ảnh thiếu alt, internal link, title/meta | Chậm |
| Google Search Console | Clicks, impressions, CTR, vị trí trung bình theo URL; trạng thái lập chỉ mục | Hàng ngày (trễ ~2 ngày) |
| Google Analytics 4 | Phiên, người dùng, thời gian tương tác, key event theo landing page | Gần realtime |
| Ahrefs Site Explorer | DR, backlink, referring domains, từ khoá, traffic, hiện diện AI | Vài ngày một lần |

## Cấu trúc

```
index.html                  Dashboard (self-contained, mở được offline)
data/
  kvy-crawl-data.csv        365 URL từ sitemap + chỉ số kỹ thuật
  kvy-gsc-data.csv          Hiệu suất GSC theo URL
  kvy-ga4-data.csv          Landing page GA4
  kvy-merged-data.csv       Bộ dữ liệu hợp nhất theo URL (nguồn của dashboard)
history/
  history.csv               Một dòng mỗi ngày, dùng vẽ biểu đồ xu hướng
  YYYY-MM-DD-merged.csv     Ảnh chụp dữ liệu hợp nhất từng ngày
scripts/
  build_v2.py               Ghép GSC vào dashboard
  build_v3.py               Ghép GA4 vào dashboard
  inject_history.py         Chèn/cập nhật khối "Xu hướng theo ngày"
```

## Cách đọc các cột trong bảng chi tiết

Đường dẫn bắt đầu bằng `~` tương đương tiền tố `/blog/`. Ngưỡng màu: xanh = đạt, cam = cần cải thiện, đỏ = cần sửa.

Cột Clicks / Impressions / CTR / Vị trí chỉ có ở các trang đạt tối thiểu 50 lượt hiển thị trong kỳ.
Cột Phiên / Tương tác chỉ có ở các trang nằm trong 100 landing page hàng đầu của GA4.
Cột Chuyển đổi hiển thị 0 cho tới khi GA4 được cấu hình key event.

## Cập nhật thủ công

Nếu lịch tự động không chạy (máy tắt, Chrome đóng), có thể yêu cầu Claude chạy lại toàn bộ quy trình bất cứ lúc nào.

## Giới hạn cần biết

- Số liệu tổng của GSC lấy theo báo cáo tổng; tổng theo cấp trang cao hơn do cách Search Console phân bổ hiển thị giữa hai cấp báo cáo.
- Phiên GA4 hiện đang bị nhiễu bởi lưu lượng referral spam. Nên đọc kèm bộ lọc trước khi dùng làm đường cơ sở.
- Điểm sức khoẻ là thang chấm nội bộ để so sánh giữa các kỳ, không phải chỉ số chính thức của Google.
