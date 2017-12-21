import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

import { RefGroup, RefDir, RefFile, Sample } from '../models/models'

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


    // get all RefGroup list
    getGroupList(): Observable<RefGroup[]> {
        return this._http.get(this.baseUrl + '/action/?action=get_refGroupList')
            .map(res => res.json());
    }

  // get top refDir by group_id
    getTopRefDir(group_id: string): Observable<RefDir[]>{
        return this._http.get(this.baseUrl + '/action/?action=get_topRefDirs&group_id=' + group_id)
            .map(res => res.json());
    }

    // get sub RefDir by RefDirId
    getSubRefDirs(refDir_id: string): Observable<RefDir[]> {
        return this._http.get(this.baseUrl + '/action/?action=get_subRefDirs&refDir_id=' + refDir_id)
            .map(res => res.json());
    }

    // get sub Sample by RefDirId
    getSubSamples(refDir_id: string): Observable<Sample[]> {
        return this._http.get(this.baseUrl + '/action/?action=get_subSamples&refDir_id=' + refDir_id)
            .map(res => res.json());
    }


    // get sub refFile by RefDirId
    getSubRefFiles(refDir_id: string): Observable<RefFile[]>{
        return this._http.get(this.baseUrl + '/action/?action=get_subRefFiles&refDir_id=' + refDir_id)
            .map(res => res.json());
    }

  doTest(): void {

  }

  // getTestData(): void {
  //     this._http.get(this.baseUrl + '/test/?a=1&b=2&c=3')
  //         .map(res => res.json());
  // }
}
