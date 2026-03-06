import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const revenueData = [
  { month: '1월', revenue: 4200 },
  { month: '2월', revenue: 5800 },
  { month: '3월', revenue: 7200 },
  { month: '4월', revenue: 8900 },
  { month: '5월', revenue: 11400 },
  { month: '6월', revenue: 13800 },
  { month: '7월', revenue: 16500 },
  { month: '8월', revenue: 19200 },
  { month: '9월', revenue: 23400 },
  { month: '10월', revenue: 27800 },
  { month: '11월', revenue: 30100 },
  { month: '12월', revenue: 32400 },
];

const ordersData = [
  { month: '1월', orders: 450 },
  { month: '2월', orders: 620 },
  { month: '3월', orders: 890 },
  { month: '4월', orders: 1120 },
  { month: '5월', orders: 1450 },
  { month: '6월', orders: 1780 },
  { month: '7월', orders: 2100 },
  { month: '8월', orders: 2450 },
  { month: '9월', orders: 2890 },
  { month: '10월', orders: 3340 },
  { month: '11월', orders: 3720 },
  { month: '12월', orders: 4140 },
];

const topCreators = [
  { name: '리아 먹방', revenue: 14805 },
  { name: '사라 헬스', revenue: 9876 },
  { name: '제이크 커피', revenue: 8234 },
  { name: '핏 마이크', revenue: 7890 },
  { name: '게이밍 프로', revenue: 8505 },
];

const topProductsData = [
  { name: '파이어 소��', sales: 2340 },
  { name: '말차 파우더', sales: 1890 },
  { name: '커피 블렌드', sales: 1650 },
  { name: '프로틴 바', sales: 1420 },
  { name: '에너지 드링크', sales: 1250 },
];

export default function Analytics() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">분석</h1>
        <p className="text-gray-600">성과 지표 및 인사이트</p>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        {/* Revenue Over Time */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">시간별 매출</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Line type="monotone" dataKey="revenue" stroke="#ea7c4d" strokeWidth={2} dot={{ fill: '#ea7c4d' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Orders Growth */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">주문 증가</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={ordersData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Line type="monotone" dataKey="orders" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Top Creators by Revenue */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">매출 상위 크리에이터</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topCreators} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis type="number" stroke="#6b7280" />
              <YAxis dataKey="name" type="category" stroke="#6b7280" width={100} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="revenue" fill="#ea7c4d" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products by Sales */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">판매량 순위 상위 제품</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topProductsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Bar dataKey="sales" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}