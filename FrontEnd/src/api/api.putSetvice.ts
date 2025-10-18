import { instance } from "./api.config";

const updateCompanyField = (inn: string, fieldKey: any)=>{
    let data = JSON.stringify(fieldKey)
    return instance.put(`api/Data/UpdateCompany/${inn}`, data)
}

const PutService = {
    updateCompanyField
};

export default PutService