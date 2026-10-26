from datetime import date
from decimal import Decimal
from app.services.financial.calculators import duplicate_groups, unique_transactions

def investigate(txs):
    flags=[{'kind':'duplicate_reference','severity':'review','classification':'confirmed_inconsistency','evidence_ids':g,'message':'Repeated account and transaction reference; counted once in metrics.'} for g in duplicate_groups(txs)]
    ts=unique_transactions(txs)
    # Bounded directed graph search, 2–4 edges, exact accounts and amount, chronological ≤3 days.
    adjacency={}
    for t in ts: adjacency.setdefault(t['from_account'],[]).append(t)
    seen=set(); budget=20000
    def walk(start,account,path,visited):
        nonlocal budget
        if len(path)>=4 or budget<=0:return
        for t in adjacency.get(account,[]):
            budget-=1
            if budget<=0:return
            if path:
                days=(date.fromisoformat(t['date'])-date.fromisoformat(path[0]['date'])).days
                if days<0 or days>3 or t['date']<path[-1]['date'] or Decimal(str(t['amount']))!=Decimal(str(path[0]['amount'])):continue
            if t['to_account']==start and path:
                chain=path+[t]; key=tuple(sorted(x['evidence_id'] for x in chain))
                if key not in seen:
                    seen.add(key); flags.append({'kind':'potential_cycle','severity':'review','classification':'unverified_suspicion','message':'Equal-value funds return through linked accounts within three days; investigate purpose.','evidence_ids':[x['evidence_id'] for x in chain], 'transactions':chain})
            elif t['to_account'] not in visited:walk(start,t['to_account'],path+[t],visited|{t['to_account']})
    for account in adjacency:walk(account,account,[],{account})
    if budget<=0:flags.append({'kind':'graph_limit','severity':'review','classification':'limitation','message':'Graph search budget reached; manual review required.','evidence_ids':[]})
    negatives=[t['evidence_id'] for t in ts if t.get('balance') is not None and Decimal(str(t['balance']))<0]
    if negatives:flags.append({'kind':'negative_balance','severity':'review','classification':'observed_fact','message':'Negative closing balances observed.','evidence_ids':negatives})
    return flags
