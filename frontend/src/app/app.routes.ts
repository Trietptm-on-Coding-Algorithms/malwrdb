import { Routes } from '@angular/router';
import { HomeComponent } from './home';
import { TestComponent } from './test';
import { SampleUploadComponent } from './sample-upload';
import { AboutComponent } from './about';
import { NoContentComponent } from './no-content';

export const ROUTES: Routes = [
  { path: '',      component: HomeComponent },
  { path: 'home',  component: HomeComponent },
  { path: 'test',  component: TestComponent },
  { path: 'sample-upload',  component: SampleUploadComponent },
  { path: 'about', component: AboutComponent },
  { path: 'detail', loadChildren: './+detail#DetailModule'},
  { path: 'barrel', loadChildren: './+barrel#BarrelModule'},
  { path: '**',    component: NoContentComponent },
];
