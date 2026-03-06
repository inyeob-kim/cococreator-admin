const factories = [
  {
    id: 1,
    name: '내추럴푸드',
    country: '한국',
    productType: '소스',
    moq: 1000,
    leadTime: 30,
    certifications: ['FDA', 'HACCP', '유기농'],
  },
  {
    id: 2,
    name: '헬스 서플먼트',
    country: '미국',
    productType: '보충제',
    moq: 500,
    leadTime: 45,
    certifications: ['FDA', 'GMP', '유기농'],
  },
  {
    id: 3,
    name: '프리미엄 커피 로스터스',
    country: '콜롬비아',
    productType: '커피',
    moq: 2000,
    leadTime: 60,
    certifications: ['공정무역', '유기농', '레인포레스트'],
  },
  {
    id: 4,
    name: '핏푸드 매뉴팩처링',
    country: '호주',
    productType: '스낵',
    moq: 3000,
    leadTime: 40,
    certifications: ['FDA', 'HACCP', 'ISO 22000'],
  },
  {
    id: 5,
    name: '베버리지텍 솔루션',
    country: '독일',
    productType: '음료',
    moq: 5000,
    leadTime: 50,
    certifications: ['FDA', 'HACCP', 'BRC'],
  },
  {
    id: 6,
    name: '아시안 푸드 프로듀서',
    country: '태국',
    productType: '식품',
    moq: 1500,
    leadTime: 35,
    certifications: ['FDA', 'HACCP', '할랄'],
  },
];

export default function Factories() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">제조사</h1>
        <p className="text-gray-600">OEM 제조사 데이터베이스 및 파트너십</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  제조사
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  국가
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  제품 유형
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  최소 주문량
                </th>
                <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  리드타임
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  인증
                </th>
              </tr>
            </thead>
            <tbody>
              {factories.map((factory) => (
                <tr key={factory.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <p className="text-sm font-medium text-gray-900">{factory.name}</p>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-gray-900">{factory.country}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800 text-xs font-medium">
                      {factory.productType}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    {factory.moq.toLocaleString()} units
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 text-right">
                    {factory.leadTime} days
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {factory.certifications.map((cert, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2 py-0.5 rounded bg-green-50 text-green-700 text-xs"
                        >
                          {cert}
                        </span>
                      ))}
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