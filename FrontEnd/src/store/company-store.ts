import { makeAutoObservable } from "mobx";
import RootStore from "./root-store";
import { ICompany } from "../Interfaces/ICompany";
import GetService from "../api/api.getService";
import PostService from "../api/api.postService";
import PutService from "../api/api.putSetvice";

class CompanyStore{
    data: ICompany[] = [];
    currentCompany: ICompany = {} as ICompany;
    root: RootStore

    constructor(root: RootStore){
    makeAutoObservable(this, {}, { autoBind: true });
    this.root = root;
    }

    setData(data: ICompany[]){
        this.data = data
    }

    setCurrentCompany(company: ICompany){
        this.currentCompany = company
    }

    async getData(){
        const response = await GetService.getAll()
        var data: ICompany[] = response.data
        console.log('first', data)
        this.setData(data)
    }

    getCompanyByInn(inn: string){
        const company = this.data.find((c: ICompany)=> c.orgFullName == inn)
        if (company) this.setCurrentCompany(company);
    }

    async createCompany(company: ICompany){
        let response = await PostService.createCompany(company)
        if (response.status<300){
            this.getData()
        }
    }

    async updateCompanyField(inn: string, key:string, value: any){
        const payload = { [key]: value };
        let response = await PutService.updateCompanyField(inn, payload)
        if (response.status<300){
            this.getCompanyByInn(inn)
        }
    }


}

export default CompanyStore;