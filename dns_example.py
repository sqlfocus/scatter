#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dns.resolver


__RESOLV = dns.resolver.Resolver()   #init, setting server ip
__RESOLV.nameservers = ["8.8.8.8"]

def get(dom, rdtype):
    '''
    param dom [string] domain, such as 'www.baidu.com'
    param rdtype [int] record type, such as 'A'/1...
    return [list] dns resolve result
    '''
    try:
        answer = __RESOLV.query(dom, rdtype) #class Answer
    except (dns.resolver.NoNameservers,dns.resolver.NoAnswer) as err:
        print(err)
        return []

    ret = []
    for reses in answer.response.answer: #class RRset
        for res in reses:                #class A/CNAME/...
            if res.rdtype != rdtype:
                continue
            ret.append(res.to_text())
    return ret

if __name__ == "__main__":
    type_val = {
        "A":1,
        "NS":2,
        "CNAME":5,
        "SOA":6,
        "PTR":12,
        "MX":15,
        "TXT":16,
        "AAAA":28,
    }
    
    print(get('baidu.com', type_val.get('A')))

    
