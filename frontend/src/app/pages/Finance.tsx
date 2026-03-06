import { DollarSign, TrendingUp, Percent } from 'lucide-react';
import { StatCard } from '../components/StatCard';

const payouts = [
  {
    id: 1,
    creator: '리아 먹방',
    revenue: 14805,
    creatorShare: 4441,
    paymentStatus: '지급완료',
    paymentDate: '2026년 3월 1일',
  },
  {
    id: 2,
    creator: '사라 헬스',
    revenue: 9876,
    creatorShare: 2962,
    paymentStatus: '지급완료',
    paymentDate: '2026년 3월 1일',
  },
  {
    id: 3,
    creator: '제이크 커피',
    revenue: 8234,
    creatorShare: 2470,
    paymentStatus: '지급완료',
    paymentDate: '2026년 3월 1일',
  },
  {
    id: 4,
    creator: '핏 마이크',
    revenue: 7890,
    creatorShare: 2367,
    paymentStatus: '대기중',
    paymentDate: '2026년 3월 15일',
  },
  {
    id: 5,
    creator: '게이밍 프로',
    revenue: 8505,
    creatorShare: 2551,
    paymentStatus: '대기중',
    paymentDate: '2026년 3월 15일',
  },
];

export default function Finance() {
  const totalRevenue = payouts.reduce((sum, p) => sum + p.revenue, 0);
  const totalCreatorPayouts = payouts.reduce((sum, p) => sum + p.creatorShare, 0);
  const platformRevenue = totalRevenue - totalCreatorPayouts;
  const avgMargin = ((platformRevenue / totalRevenue) * 100).toFixed(1);

  const getStatusColor = (status: string) => {
    return status === '지급완료' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800';
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">재무</h1>
        <p className="text-gray-600">재무 개요 및 크리에이터 지급</p>
      </div>

      {/* Financial Summary */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        <StatCard
          title="플랫폼 수익"
          value={`$${platformRevenue.toLocaleString()}`}
          icon={DollarSign}
        />
        <StatCard
          title="크리에이터 지급"
          value={`$${totalCreatorPayouts.toLocaleString()}`}
          icon={TrendingUp}
        />
        <StatCard
          title="평균 제품 마진"
          value={`${avgMargin}%`}
          icon={Percent}
        />
      </div>

      {/* Payout Table */}
      <div className="bg-white rounded-xl border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">크리에이터 지급 내역</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  매출
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터 수익 (30%)
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  지급 상태
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  지급일
                </th>
              </tr>
            </thead>
            <tbody>
              {payouts.map((payout) => (
                <tr key={payout.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white font-medium">
                        {payout.creator.charAt(0)}
                      </div>
                      <span className="text-sm font-medium text-gray-900">{payout.creator}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    ${payout.revenue.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 text-right">
                    ${payout.creatorShare.toLocaleString()}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(payout.paymentStatus)}`}>
                      {payout.paymentStatus}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{payout.paymentDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}