import { useStores } from "./context/root-store-context.ts";
import { observer } from "mobx-react-lite";
import { ReactNotifications } from "react-notifications-component";
import "react-notifications-component/dist/theme.css";
import { Flowbite } from "flowbite-react";
import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./router/private.route.tsx";


const App = () => {
  const {
  } = useStores();



  return (
    <BrowserRouter>
    <Flowbite>
      <div className="app-container h-screen bg-white dark:bg-gray-700">
        <ReactNotifications />
          <AppRoutes />
      </div>
    </Flowbite >
      </BrowserRouter>
  );
};

export default observer(App);
