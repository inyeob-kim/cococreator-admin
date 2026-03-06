const orders = [
  {
    id: 1,
    product: '파이어 소스',
    creator: '리아 먹방',
    orders: 2340,
    revenue: 11466,
    creatorShare: 3439,
    platformFee: 1146,
  },
  {
    id: 2,
    product: '말차 파우더',
    creator: '사라 헬스',
    orders: 1890,
    revenue: 9876,
    creatorShare: 2962,
    platformFee: 987,
  },
  {
    id: 3,
    product: '커피 블렌드',
    creator: '제이크 커피',
    orders: 1650,
    revenue: 8234,
    creatorShare: 2470,
    platformFee: 823,
  },
  {
    id: 4,
    product: '프로틴 바',
    creator: '핏 마이크',
    orders: 1420,
    revenue: 7890,
    creatorShare: 2367,
    platformFee: 789,
  },
  {
    id: 5,
    product: '에너지 드링크',
    creator: '게이밍 프로',
    orders: 1250,
    revenue: 6543,
    creatorShare: 1962,
    platformFee: 654,
  },
  {
    id: 6,
    product: '매운 라면',
    creator: '리아 먹방',
    orders: 890,
    revenue: 4532,
    creatorShare: 1359,
    platformFee: 453,
  },
];

export default function Orders() {
  const totals = {
    orders: orders.reduce((sum, order) => sum + order.orders, 0),
    revenue: orders.reduce((sum, order) => sum + order.revenue, 0),
    creatorShare: orders.reduce((sum, order) => sum + order.creatorShare, 0),
    platformFee: orders.reduce((sum, order) => sum + order.platformFee, 0),
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">주문</h1>
        <p className="text-gray-600">판매 추적 및 매출 관리</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-sm text-gray-600 mb-1">총 주문</p>
          <p className="text-2xl font-semibold text-gray-900">{totals.orders.toLocaleString()}</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-sm text-gray-600 mb-1">총 매출</p>
          <p className="text-2xl font-semibold text-gray-900">${totals.revenue.toLocaleString()}</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-sm text-gray-600 mb-1">크리에이터 수익</p>
          <p className="text-2xl font-semibold text-gray-900">
            ${totals.creatorShare.toLocaleString()}
          </p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <p className="text-sm text-gray-600 mb-1">플랫폼 수수료</p>
          <p className="text-2xl font-semibold text-gray-900">
            ${totals.platformFee.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Orders Table */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  제품
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  주문
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  매출
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터 수익
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  플랫폼 수수료
                </th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">{order.product}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                        {order.creator.charAt(0)}
                      </div>
                      <span className="text-sm text-gray-900">{order.creator}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    {order.orders.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    ${order.revenue.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    ${order.creatorShare.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600 text-right">
                    ${order.platformFee.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}