import { Injectable } from '@angular/core';
// import { Http, Response } from '@angular/http';
import { HttpClient } from "@angular/common/http";

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

import { LogLine, RefGroup, RefDir, RefFile, Sample } from '../models/models'

@Injectable()
export class ServerDataService {

  baseUrl: string = 'http://127.0.0.1:5000'

  constructor(private _http: HttpClient) {

  }

    // -----------------------------------------------------------------------------------

    // get logLine list
    getLogLines(isWarn: boolean, isDebug: boolean): Observable<LogLine[]>{
        return this._http.get<LogLine[]>(this.baseUrl + '/logline/?action=get_logLines&isWarn=' + isWarn + "&isDebug=" + isDebug);
    }

    // clear log lines
    clearLogLines(){
      // .subscribe() is necessary to truely "send" this request!!!
        this._http.get(this.baseUrl + '/logline/?action=clearLogLines').subscribe(data => {
            // console.log(data);
        });
    }

    // -----------------------------------------------------------------------------------

    // get list stuff

    // get all RefGroup list
    getGroupList(pageSize: number, pageIndex: number): Observable<RefGroup[]> {
        return this._http.get<RefGroup[]>(this.baseUrl + '/action/?action=get_refGroupList&pageSize=' + pageSize + "&pageIndex=" + pageIndex);
    }

  // get top refDir by group_id
    getTopRefDir(group_id: string): Observable<RefDir[]>{
        return this._http.get<RefDir[]>(this.baseUrl + '/action/?action=get_topRefDirs&group_id=' + group_id);
    }

    // get sub RefDir by RefDirId
    getSubRefDirs(refDir_id: string): Observable<RefDir[]> {
        return this._http.get<RefDir[]>(this.baseUrl + '/action/?action=get_subRefDirs&refDir_id=' + refDir_id);
    }

    // get sub Sample by RefDirId
    getSubSamples(refDir_id: string): Observable<Sample[]> {
        return this._http.get<Sample[]>(this.baseUrl + '/action/?action=get_subSamples&refDir_id=' + refDir_id);
    }


    // get sub refFile by RefDirId
    getSubRefFiles(refDir_id: string): Observable<RefFile[]>{
        return this._http.get<RefFile[]>(this.baseUrl + '/action/?action=get_subRefFiles&refDir_id=' + refDir_id);
    }

    // -----------------------------------------------------------------------------------

    // sample/file

    // analyze file as sample
    cmdAnalyzeSample(refFile_id: string){
      this._http.get(this.baseUrl + '/action/?action=analyzeAsSample&refFileId=' + refFile_id).subscribe();
    }

    // -----------------------------------------------------------------------------------

  doTest(): void {

  }

}
