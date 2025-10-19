import axios from "axios"
import { ICompany } from "../Interfaces/ICompany"
import { instance } from "./api.config"

const createCompany = (company: ICompany)=>{
    let data = JSON.stringify(
        company
    )
    return instance.post(`api/Data/AddCompany`, data)
}

const uploadExcelWithCompnanies = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  return instance.post(`/ImportFromExcel`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

const uploadPdfFile = async (file: File)=>{
  const formData = new FormData();
  formData.append("file", file);
    const res = await axios.post("http://localhost:8000/api/v1/parse-pdf/", formData, {
      headers: {
      "Content-Type": "multipart/form-data",
    },
    })
}


const PostService = {
    createCompany,
    uploadExcelWithCompnanies,
    uploadPdfFile
}

export default PostService;