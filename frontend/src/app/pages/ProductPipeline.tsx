import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { useState } from 'react';

const ITEM_TYPE = 'PRODUCT_CARD';

interface Product {
  id: number;
  name: string;
  creator: string;
  stage: string;
}

const initialProducts: Product[] = [
  { id: 1, name: '파이어 소스', creator: '리아 먹방', stage: '생산' },
  { id: 2, name: '말차 파우더', creator: '사라 헬스', stage: '출시' },
  { id: 3, name: '커피 블렌드', creator: '제이크 커피', stage: '출시' },
  { id: 4, name: '프로틴 바', creator: '핏 마이크', stage: 'OEM 협상' },
  { id: 5, name: '에너지 드링크', creator: '게이밍 프로', stage: '샘플링' },
  { id: 6, name: '매운 라면', creator: '리아 먹방', stage: '조사' },
  { id: 7, name: '요가 매트', creator: '사라 헬스', stage: '아이디어' },
  { id: 8, name: '게이밍 의자', creator: '게이밍 프로', stage: '아이디어' },
];

const stages = ['아이디어', '조사', '샘플링', 'OEM 협상', '생산', '출시'];

interface ProductCardProps {
  product: Product;
}

function ProductCard({ product }: ProductCardProps) {
  const [{ isDragging }, drag] = useDrag({
    type: ITEM_TYPE,
    item: { id: product.id },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  return (
    <div
      ref={drag}
      className={`bg-white border border-gray-200 rounded-lg p-4 mb-3 cursor-move hover:shadow-md transition-shadow ${
        isDragging ? 'opacity-50' : ''
      }`}
    >
      <h4 className="text-sm font-medium text-gray-900 mb-2">{product.name}</h4>
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white text-xs">
          {product.creator.charAt(0)}
        </div>
        <p className="text-xs text-gray-600">{product.creator}</p>
      </div>
    </div>
  );
}

interface StageColumnProps {
  stage: string;
  products: Product[];
  onDrop: (productId: number, stage: string) => void;
}

function StageColumn({ stage, products, onDrop }: StageColumnProps) {
  const [{ isOver }, drop] = useDrop({
    accept: ITEM_TYPE,
    drop: (item: { id: number }) => onDrop(item.id, stage),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  });

  return (
    <div
      ref={drop}
      className={`bg-gray-50 rounded-xl p-4 min-h-[500px] ${
        isOver ? 'ring-2 ring-orange-500 bg-orange-50' : ''
      }`}
    >
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-900">{stage}</h3>
        <p className="text-xs text-gray-500 mt-1">{products.length}개 제품</p>
      </div>
      <div>
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}

function ProductPipelineContent() {
  const [products, setProducts] = useState<Product[]>(initialProducts);

  const handleDrop = (productId: number, newStage: string) => {
    setProducts((prev) =>
      prev.map((p) => (p.id === productId ? { ...p, stage: newStage } : p))
    );
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">제품 파이프라인</h1>
        <p className="text-gray-600">각 단계별 제품 개발 추적</p>
      </div>

      <div className="grid grid-cols-6 gap-4">
        {stages.map((stage) => (
          <StageColumn
            key={stage}
            stage={stage}
            products={products.filter((p) => p.stage === stage)}
            onDrop={handleDrop}
          />
        ))}
      </div>
    </div>
  );
}

export default function ProductPipeline() {
  return (
    <DndProvider backend={HTML5Backend}>
      <ProductPipelineContent />
    </DndProvider>
  );
}