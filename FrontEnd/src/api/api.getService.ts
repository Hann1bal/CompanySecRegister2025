import { ICompany } from "../Interfaces/ICompany";
import { instance } from "./api.config"

const getAll = () =>{
    return instance.get<ICompany[]>("/api/Data/GetAll")
}

const GetService = {
    getAll
}

export default GetService;