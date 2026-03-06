import { useState } from 'react';
import { Eye, X } from 'lucide-react';

const creators = [
  {
    id: 1,
    name: '리아 먹방',
    subscribers: '32만',
    country: '인도네시아',
    category: '먹방',
    avgViews: '4.5만',
    status: '협상중',
    channel: '@riamukbang',
    engagementRate: '8.2%',
    primaryAudience: '동남아시아',
    ageRange: '18-34',
    productIdeas: ['파이어 소스', '매운 라면', '조리 도구'],
  },
  {
    id: 2,
    name: '사라 헬스',
    subscribers: '58만',
    country: '미국',
    category: '헬스 & 웰니스',
    avgViews: '9.2만',
    status: '파트너',
    channel: '@sarahhealthlife',
    engagementRate: '12.5%',
    primaryAudience: '북미',
    ageRange: '25-44',
    productIdeas: ['말차 파우더', '단백질 보충제', '요가 매트'],
  },
  {
    id: 3,
    name: '제이크 커피',
    subscribers: '21만',
    country: '영국',
    category: '커피 & 라이프스타일',
    avgViews: '3.8만',
    status: '파트너',
    channel: '@jakecoffeemorning',
    engagementRate: '9.8%',
    primaryAudience: '유럽',
    ageRange: '22-45',
    productIdeas: ['커피 블렌드', '프렌치 프레스', '커피 그라인더'],
  },
  {
    id: 4,
    name: '핏 마이크',
    subscribers: '45만',
    country: '호주',
    category: '피트니스',
    avgViews: '6.7만',
    status: '파트너',
    channel: '@fitmikeworkout',
    engagementRate: '11.3%',
    primaryAudience: '오세아니아',
    ageRange: '20-40',
    productIdeas: ['프로틴 바', '저항 밴드', '쉐이커 보틀'],
  },
  {
    id: 5,
    name: '게이밍 프로',
    subscribers: '89만',
    country: '미국',
    category: '게임',
    avgViews: '12.5만',
    status: '연락완료',
    channel: '@gamingpromax',
    engagementRate: '14.2%',
    primaryAudience: '글로벌',
    ageRange: '16-30',
    productIdeas: ['에너지 드링크', '게이밍 의자', 'LED 조명'],
  },
];

export default function Creators() {
  const [selectedCreator, setSelectedCreator] = useState<typeof creators[0] | null>(null);

  const getStatusColor = (status: string) => {
    switch (status) {
      case '파트너':
        return 'bg-green-100 text-green-800';
      case '협상중':
        return 'bg-orange-100 text-orange-800';
      case '연락완료':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">크리에이터</h1>
        <p className="text-gray-600">크리에이터 파트너십 관리</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  크리에이터명
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  구독자
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  국가
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  카테고리
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  평균 조회수
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  상태
                </th>
                <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-4">
                  작업
                </th>
              </tr>
            </thead>
            <tbody>
              {creators.map((creator) => (
                <tr key={creator.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white font-medium">
                        {creator.name.charAt(0)}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">{creator.name}</p>
                        <p className="text-xs text-gray-500">{creator.channel}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{creator.subscribers}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{creator.country}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{creator.category}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{creator.avgViews}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(creator.status)}`}>
                      {creator.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => setSelectedCreator(creator)}
                      className="text-orange-600 hover:text-orange-700 text-sm font-medium flex items-center gap-1"
                    >
                      <Eye className="w-4 h-4" />
                      보기
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Creator Profile Panel */}
      {selectedCreator && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">크리에이터 프로필</h2>
              <button
                onClick={() => setSelectedCreator(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Header */}
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white text-2xl font-medium">
                  {selectedCreator.name.charAt(0)}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{selectedCreator.name}</h3>
                  <p className="text-sm text-gray-600">{selectedCreator.channel}</p>
                </div>
              </div>

              {/* Channel Statistics */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">채널 통계</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 mb-1">구독자</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedCreator.subscribers}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 mb-1">평균 조회수</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedCreator.avgViews}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 mb-1">참여율</p>
                    <p className="text-lg font-semibold text-gray-900">{selectedCreator.engagementRate}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-xs text-gray-600 mb-1">상태</p>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(selectedCreator.status)}`}>
                      {selectedCreator.status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Audience Insights */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">청중 인사이트</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between py-2 border-b border-gray-100">
                    <span className="text-sm text-gray-600">주요 시청자</span>
                    <span className="text-sm font-medium text-gray-900">{selectedCreator.primaryAudience}</span>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-gray-100">
                    <span className="text-sm text-gray-600">연령대</span>
                    <span className="text-sm font-medium text-gray-900">{selectedCreator.ageRange}</span>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b border-gray-100">
                    <span className="text-sm text-gray-600">카테고리</span>
                    <span className="text-sm font-medium text-gray-900">{selectedCreator.category}</span>
                  </div>
                </div>
              </div>

              {/* Product Ideas */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">제품 아이디어</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedCreator.productIdeas.map((idea, index) => (
                    <span
                      key={index}
                      className="px-3 py-1.5 bg-orange-50 text-orange-700 rounded-lg text-sm"
                    >
                      {idea}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}