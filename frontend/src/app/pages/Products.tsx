const products = [
  {
    id: 1,
    name: '파이어 소스',
    category: '소스',
    cogs: 1.2,
    retailPrice: 4.9,
    margin: 47,
    creator: '리아 먹방',
    sku: 'FS-001',
  },
  {
    id: 2,
    name: '말차 파우더',
    category: '보충제',
    cogs: 3.5,
    retailPrice: 12.9,
    margin: 52,
    creator: '사라 헬스',
    sku: 'MP-001',
  },
  {
    id: 3,
    name: '커피 블렌드',
    category: '커피',
    cogs: 2.8,
    retailPrice: 8.9,
    margin: 45,
    creator: '제이크 커피',
    sku: 'CB-001',
  },
  {
    id: 4,
    name: '프로틴 바',
    category: '스낵',
    cogs: 1.5,
    retailPrice: 3.9,
    margin: 38,
    creator: '핏 마이크',
    sku: 'PB-001',
  },
  {
    id: 5,
    name: '에너지 드링크',
    category: '음료',
    cogs: 1.8,
    retailPrice: 4.9,
    margin: 41,
    creator: '게이밍 프로',
    sku: 'ED-001',
  },
  {
    id: 6,
    name: '매운 라면',
    category: '식품',
    cogs: 0.9,
    retailPrice: 2.9,
    margin: 43,
    creator: '리아 먹방',
    sku: 'SN-001',
  },
];

export default function Products() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">제품</h1>
        <p className="text-gray-600">모든 크리에이터 제품 및 가격 관리</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  제품
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  카테고리
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  원가
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  소비자가
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  마진
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터
                </th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{product.name}</p>
                      <p className="text-xs text-gray-500 mt-1">SKU: {product.sku}</p>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-800 text-xs font-medium">
                      {product.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    ${product.cogs.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    ${product.retailPrice.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-green-100 text-green-800 text-xs font-medium">
                      {product.margin}%
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                        {product.creator.charAt(0)}
                      </div>
                      <span className="text-sm text-gray-900">{product.creator}</span>
                    </div>
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