import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

import {Sample} from '../models/sample'

@Injectable()
export class ServerDataService {

    baseUrl: string = 'http://127.0.0.1:5000'

    constructor(private _http: Http) {

    }

    // 获取样本数目
    // getSampleCount(): number{
    //     this._http.get(this.baseUrl + '/sample/action/?action=count&type=all&author=all')
    //         .map(res => res.json);
    // }

    // 获取样本列表
    getSampleList(): Observable<Sample[]> {
        return this._http.get(this.baseUrl + '/sample/action/?action=list&type=all&author=all')
            .map(res => res.json());
    }

    doTest(): void{
        // this.getSampleCount()
        this.getSampleList()
    }

    // getTestData(): void {
    //     this._http.get(this.baseUrl + '/test/?a=1&b=2&c=3')
    //         .map(res => res.json());
    // }
}
