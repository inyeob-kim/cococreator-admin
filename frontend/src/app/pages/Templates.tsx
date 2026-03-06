const templates = [
  {
    id: 1,
    name: '파이어 소스 템플릿',
    category: '소스',
    flavorOptions: ['극강 매운맛', '스위트 칠리', '갈릭'],
    baseCost: 1.2,
    image: 'sauce',
  },
  {
    id: 2,
    name: '말차 파우더 템플릿',
    category: '보충제',
    flavorOptions: ['오리지널', '바닐라', '세리모니얼 등급'],
    baseCost: 3.5,
    image: 'matcha',
  },
  {
    id: 3,
    name: '커피 블렌드 템플릿',
    category: '커피',
    flavorOptions: ['라이트 로스트', '미디엄 로스트', '다크 로스트', '에스프레소'],
    baseCost: 2.8,
    image: 'coffee',
  },
  {
    id: 4,
    name: '프로틴 바 템플릿',
    category: '스낵',
    flavorOptions: ['초콜릿', '땅콩버터', '바닐라', '베리'],
    baseCost: 1.5,
    image: 'protein',
  },
  {
    id: 5,
    name: '에너지 드링크 템플릿',
    category: '음료',
    flavorOptions: ['트로피컬', '베리 블라스트', '시트러스', '무설탕'],
    baseCost: 1.8,
    image: 'energy',
  },
  {
    id: 6,
    name: '티 블렌드 템플릿',
    category: '음료',
    flavorOptions: ['녹차', '홍차', '허브', '우롱'],
    baseCost: 2.1,
    image: 'tea',
  },
];

export default function Templates() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">템플릿</h1>
        <p className="text-gray-600">빠른 브랜드 론칭을 위한 제품 템플릿 라이브러리</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {templates.map((template) => (
          <div
            key={template.id}
            className="bg-white border border-gray-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div className="h-48 bg-gradient-to-br from-orange-100 to-orange-200 flex items-center justify-center">
              <div className="text-6xl">
                {template.image === 'sauce' && '🌶️'}
                {template.image === 'matcha' && '🍵'}
                {template.image === 'coffee' && '☕'}
                {template.image === 'protein' && '🍫'}
                {template.image === 'energy' && '⚡'}
                {template.image === 'tea' && '🫖'}
              </div>
            </div>
            <div className="p-6">
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{template.name}</h3>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-800 text-xs font-medium">
                  {template.category}
                </span>
              </div>

              <div className="mb-4">
                <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">맛 옵션</p>
                <div className="flex flex-wrap gap-2">
                  {template.flavorOptions.map((flavor, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-orange-50 text-orange-700 rounded text-xs"
                    >
                      {flavor}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">기본 원가</span>
                  <span className="text-lg font-semibold text-gray-900">
                    ${template.baseCost.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}