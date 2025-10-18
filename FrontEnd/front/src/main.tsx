import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { RootStoreContext } from './context/root-store-context.ts'
import RootStore from './store/root-store.ts'
import { ReactFlowProvider } from 'reactflow'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <RootStoreContext.Provider value={new RootStore()}>
    <ReactFlowProvider>

      <App />
    </ReactFlowProvider>
  </RootStoreContext.Provider>
)
