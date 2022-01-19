import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Log } from '../lib/model/Log';
import { Request } from '../lib/model/Request';
import { VmDataMap } from '../lib/model/VmDataMap';

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  constructor(private http: HttpClient) { }

  getVmData(): Observable<VmDataMap> {
    const url = `${environment.apiUrl}/monitor`;
    return this.http.get<VmDataMap>(url);
  }

  configure(vmNumber: number): Observable<VmDataMap> {
    const url = `${environment.apiUrl}/configure`;
    return this.http.post<VmDataMap>(url, { vm_number: vmNumber });
  }

  sendRequest(request: Request): Observable<VmDataMap> {
    const url = `${environment.apiUrl}/send`;
    return this.http.post<VmDataMap>(url, request);
  }

  getLogs(): Observable<Log[]> {
    const url = `${environment.apiUrl}/logs`;
    return this.http.get<Log[]>(url);
  }
}
