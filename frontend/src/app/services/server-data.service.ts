import { Injectable } from '@angular/core';
// import { Http, Response } from '@angular/http';
import { HttpClient, HttpParams } from "@angular/common/http";

import { Observable } from 'rxjs/Observable';

import { LogLine, RefGroup, RefDir, RefFile, Sample } from '../models/models'

@Injectable()
export class ServerDataService {

    baseUrl: string = 'http://127.0.0.1:5000'

    constructor(private _http: HttpClient) {

    }
    // -----------------------------------------------------------------------------------

    // get logLine list
    getLogLines(isWarn: boolean, isDebug: boolean): Observable<LogLine[]> {
        let params = new HttpParams();
        params = params.append("action", 'get_logLines');

        params = params.append("isWarn", `${isWarn}`);
        params = params.append("isDebug", `${isDebug}`);

        return this._http.get<LogLine[]>(this.baseUrl + "/logline/", { params: params });
    }

    // clear log lines
    clearLogLines() {
        // .subscribe() is necessary to truely "send" this request!!!
        this._http.post(this.baseUrl + "/logline/", {
            "action": "clearLogLines",
        }).subscribe();
    }

    // -----------------------------------------------------------------------------------

    // get list stuff

    // get all RefGroup list
    getGroupList(pageSize: number, pageIndex: number): Observable<RefGroup[]> {
        let params = new HttpParams();
        params = params.append("action", 'get_refGroupList');

        params = params.append("pageSize", `${pageSize}`);
        params = params.append("pageIndex", `${pageIndex}`);

        return this._http.get<RefGroup[]>(this.baseUrl + "/action/", { params: params });
    }

    // get top refDir by group_id
    getTopRefDir(group_id: string): Observable<RefDir[]> {
        let params = new HttpParams();
        params = params.append("action", 'get_topRefDirs');

        params = params.append("group_id", group_id);

        return this._http.get<RefDir[]>(this.baseUrl + "/action/", { params: params });
    }

    // get sub RefDir by RefDirId
    getSubRefDirs(refDir_id: string): Observable<RefDir[]> {
        let params = new HttpParams();
        params = params.append("action", 'get_subRefDirs');

        params = params.append("refDir_id", refDir_id);

        return this._http.get<RefDir[]>(this.baseUrl + "/action/", { params: params });
    }

    // get sub Sample by RefDirId
    getSubSamples(refDir_id: string): Observable<Sample[]> {
        let params = new HttpParams();
        params = params.append("action", 'get_subSamples');

        params = params.append("refDir_id", refDir_id);

        return this._http.get<Sample[]>(this.baseUrl + "/action/", { params: params });
    }


    // get sub refFile by RefDirId
    getSubRefFiles(refDir_id: string): Observable<RefFile[]> {
        let params = new HttpParams();
        params = params.append("action", 'get_subRefFiles');

        params = params.append("refDir_id", refDir_id);

        return this._http.get<RefFile[]>(this.baseUrl + "/action/", { params: params });
    }

    // -----------------------------------------------------------------------------------

    // sample/file

    // analyze file as sample
    cmdAnalyzeSample(refFile_id: string) {
        this._http.post(this.baseUrl + "/reffile/", {
            "action": "analyzeAsSample",
            "refFileId": refFile_id,
        }).subscribe();
    }

    // -----------------------------------------------------------------------------------

    doTest(): void {

    }

}
