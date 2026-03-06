import { StatCard } from '../components/StatCard';
import { Users, Store, Package, DollarSign } from 'lucide-react';

const pipelineStages = [
  { name: '리드', count: 8, color: 'bg-gray-200' },
  { name: '연락완료', count: 5, color: 'bg-blue-200' },
  { name: '협상중', count: 3, color: 'bg-orange-200' },
  { name: '파트너', count: 12, color: 'bg-green-200' },
];

const topProducts = [
  { product: '파이어 소스', creator: '리아 먹방', orders: 2340, revenue: 11466, margin: 47 },
  { product: '말차 파우더', creator: '사라 헬스', orders: 1890, revenue: 9876, margin: 52 },
  { product: '커피 블렌드', creator: '제이크 커피', orders: 1650, revenue: 8234, margin: 45 },
  { product: '프로틴 바', creator: '핏 마이크', orders: 1420, revenue: 7890, margin: 38 },
  { product: '에너지 드링크', creator: '게이밍 프로', orders: 1250, revenue: 6543, margin: 41 },
];

export default function Dashboard() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">대시보드</h1>
        <p className="text-gray-600">플랫폼 개요 및 주요 지표</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <StatCard
          title="전체 크리에이터"
          value="12"
          icon={Users}
          trend={{ value: '이번 달 +2', positive: true }}
        />
        <StatCard
          title="활성 브랜드"
          value="3"
          icon={Store}
          trend={{ value: '이번 달 +1', positive: true }}
        />
        <StatCard
          title="출시된 제품"
          value="5"
          icon={Package}
        />
        <StatCard
          title="총 매출"
          value="$32,400"
          icon={DollarSign}
          trend={{ value: '+12.5%', positive: true }}
        />
      </div>

      {/* Creator Pipeline */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">크리에이터 파이프라인</h2>
        <div className="flex items-center gap-4">
          {pipelineStages.map((stage, index) => (
            <div key={stage.name} className="flex-1">
              <div className={`${stage.color} rounded-lg p-4 text-center`}>
                <p className="text-sm text-gray-600 mb-1">{stage.name}</p>
                <p className="text-2xl font-semibold text-gray-900">{stage.count}</p>
              </div>
              {index < pipelineStages.length - 1 && (
                <div className="flex justify-center my-4">
                  <div className="w-8 h-0.5 bg-gray-300"></div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Top Products */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">인기 제품</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider pb-3">
                  제품
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider pb-3">
                  크리에이터
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider pb-3">
                  주문
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider pb-3">
                  매출
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider pb-3">
                  마진
                </th>
              </tr>
            </thead>
            <tbody>
              {topProducts.map((product, index) => (
                <tr key={index} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="py-4 text-sm font-medium text-gray-900">{product.product}</td>
                  <td className="py-4 text-sm text-gray-600">{product.creator}</td>
                  <td className="py-4 text-sm text-gray-900 text-right">
                    {product.orders.toLocaleString()}
                  </td>
                  <td className="py-4 text-sm text-gray-900 text-right">
                    ${product.revenue.toLocaleString()}
                  </td>
                  <td className="py-4 text-sm text-right">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-green-100 text-green-800 text-xs font-medium">
                      {product.margin}%
                    </span>
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