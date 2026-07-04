import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { MenuProvider } from './context/MenuContext'
import { CartProvider } from './context/CartContext'
import Layout from './components/Layout'
import Home from './pages/Home'
import KumpirBuilder from './pages/KumpirBuilder'
import CornBuilder from './pages/CornBuilder'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'
import OrderTrack from './pages/OrderTrack'
import MyOrders from './pages/MyOrders'
import StampCard from './pages/StampCard'
import Offers from './pages/Offers'

function App() {
  return (
    <MenuProvider>
      <CartProvider>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/kumpir" element={<KumpirBuilder />} />
              <Route path="/corn" element={<CornBuilder />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/checkout" element={<Checkout />} />
              <Route path="/orders" element={<MyOrders />} />
              <Route path="/orders/:id" element={<OrderTrack />} />
              <Route path="/stamps" element={<StampCard />} />
              <Route path="/offers" element={<Offers />} />
            </Routes>
          </Layout>
        </BrowserRouter>
      </CartProvider>
    </MenuProvider>
  )
}

export default App
