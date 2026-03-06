const brands = [
  {
    id: 1,
    brandName: 'RIA 파이어 소스',
    creator: '리아 먹방',
    product: '매운 소스',
    status: '기획중',
    launchDate: '2026년 3분기',
    description: '극강의 매운맛을 자랑하는 인도네시아 핫소스',
  },
  {
    id: 2,
    brandName: '사라 헬스 리빙',
    creator: '사라 헬스',
    product: '말차 파우더',
    status: '출시됨',
    launchDate: '2026년 1분기',
    description: '건강을 생각하는 소비자를 위한 프리미엄 유기농 말차',
  },
  {
    id: 3,
    brandName: '제이크 커피',
    creator: '제이크 커피',
    product: '커피 블렌드',
    status: '출시됨',
    launchDate: '2025년 4분기',
    description: '지속 가능한 농장에서 생산된 장인의 커피 블렌드',
  },
  {
    id: 4,
    brandName: '핏 마이크 뉴트리션',
    creator: '핏 마이크',
    product: '프로틴 바',
    status: '생산중',
    launchDate: '2026년 2분기',
    description: '천연 재료로 만든 고단백 바',
  },
  {
    id: 5,
    brandName: '게이밍 프로 에너지',
    creator: '게이밍 프로',
    product: '에너지 드링크',
    status: '샘플링',
    launchDate: '2026년 4분기',
    description: '게이머를 위한 제로 슈가 에너지 드링크',
  },
];

export default function Brands() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case '출시됨':
        return 'bg-green-100 text-green-800';
      case '생산중':
        return 'bg-blue-100 text-blue-800';
      case '샘플링':
        return 'bg-purple-100 text-purple-800';
      case '기획중':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">브랜드</h1>
        <p className="text-gray-600">크리에이터 제품 브랜드 및 상태</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  브랜드명
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  제품
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  상태
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  출시일
                </th>
              </tr>
            </thead>
            <tbody>
              {brands.map((brand) => (
                <tr key={brand.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{brand.brandName}</p>
                      <p className="text-xs text-gray-500 mt-1">{brand.description}</p>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                        {brand.creator.charAt(0)}
                      </div>
                      <span className="text-sm text-gray-900">{brand.creator}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{brand.product}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(brand.status)}`}>
                      {brand.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{brand.launchDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}