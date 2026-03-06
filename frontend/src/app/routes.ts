import { createBrowserRouter } from 'react-router';
import { Layout } from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Creators from './pages/Creators';
import Brands from './pages/Brands';
import ProductPipeline from './pages/ProductPipeline';
import Products from './pages/Products';
import Templates from './pages/Templates';
import Factories from './pages/Factories';
import Orders from './pages/Orders';
import Analytics from './pages/Analytics';
import Finance from './pages/Finance';

export const router = createBrowserRouter([
  {
    path: '/',
    Component: Login,
  },
  {
    path: '/',
    Component: Layout,
    children: [
      { path: 'dashboard', Component: Dashboard },
      { path: 'creators', Component: Creators },
      { path: 'brands', Component: Brands },
      { path: 'product-pipeline', Component: ProductPipeline },
      { path: 'products', Component: Products },
      { path: 'templates', Component: Templates },
      { path: 'factories', Component: Factories },
      { path: 'orders', Component: Orders },
      { path: 'analytics', Component: Analytics },
      { path: 'finance', Component: Finance },
    ],
  },
]);