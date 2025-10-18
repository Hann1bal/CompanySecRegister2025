import { ICompany } from "../Interfaces/ICompany"
import { instance } from "./api.config"

const createCompany = (company: ICompany)=>{
    let data = JSON.stringify(
        company
    )
    return instance.post(`api/Data/AddCompany`, data)
}

const PostService = {
    createCompany
}

export default PostService;