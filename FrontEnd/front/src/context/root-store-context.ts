import RootStore from "../store/root-store";
import { createContext, useContext } from "react";

export const RootStoreContext = createContext<RootStore | null>(null);

export const useStores = () => {
    const context = useContext(RootStoreContext);
    if (context == null) throw new Error("no provider")
    return context;
}