import { Injectable } from '@angular/core';

import { Sample } from '../models/models'

@Injectable()
export class SharedDataService {
  // 样本列表
  private _sample_list: Sample[];
  get sample_list(): Sample[]{
    return this._sample_list;
  }
  set sample_list(s_list: Sample[]){
    this._sample_list = s_list;
  }

  // 当前选中的样本
  private _currentSample: Sample;
  get currentSample(): Sample {
    if (this._currentSample == undefined && this._sample_list !== undefined && this._sample_list.length != 0){
      this._currentSample = this._sample_list[0];
    }
    return this._currentSample;
  }
  set currentSample(sample: Sample) {
    if (this._currentSample.sha256 != sample.sha256) {
      this._currentSample = sample;
    }
  }
}
