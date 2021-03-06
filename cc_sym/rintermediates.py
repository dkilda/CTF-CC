#!/usr/bin/env python
#
# Author: Yang Gao <younggao1994@gmail.com>
#
def cc_Foo(t1, t2, eris):
    lib = eris.lib
    Fki  = 2*lib.einsum('kcld,ilcd->ki', eris.ovov, t2)
    Fki -= lib.einsum('kdlc,ilcd->ki', eris.ovov, t2)
    tmp  = lib.einsum('kcld,ld->kc', eris.ovov, t1)
    Fki += 2*lib.einsum('kc,ic->ki', tmp, t1)
    tmp  = lib.einsum('kdlc,ld->kc', eris.ovov, t1)
    Fki -= lib.einsum('kc,ic->ki', tmp, t1)
    Fki += eris.foo
    return Fki

def cc_Fvv(t1, t2, eris):
    lib = eris.lib
    Fac  =-2*lib.einsum('kcld,klad->ac', eris.ovov, t2)
    Fac +=   lib.einsum('kdlc,klad->ac', eris.ovov, t2)
    tmp  =   lib.einsum('kcld,ld->kc', eris.ovov, t1)
    Fac -= 2*lib.einsum('kc,ka->ac', tmp, t1)
    tmp  =   lib.einsum('kdlc,ld->kc', eris.ovov, t1)
    Fac +=   lib.einsum('kc,ka->ac', tmp, t1)
    Fac +=   eris.fvv
    return Fac

def cc_Fov(t1, t2, eris):
    lib = eris.lib
    Fkc  = 2*lib.einsum('kcld,ld->kc', eris.ovov, t1)
    Fkc -=   lib.einsum('kdlc,ld->kc', eris.ovov, t1)
    Fkc +=   eris.fov
    return Fkc

### Eqs. (40)-(41) "lambda"

def Loo(t1, t2, eris):
    lib = eris.lib
    Lki = cc_Foo(t1, t2, eris) + lib.einsum('kc,ic->ki',eris.fov, t1)
    Lki += 2*lib.einsum('kilc,lc->ki', eris.ooov, t1)
    Lki -=   lib.einsum('likc,lc->ki', eris.ooov, t1)
    return Lki

def Lvv(t1, t2, eris):
    lib = eris.lib
    Lac = cc_Fvv(t1, t2, eris) - lib.einsum('kc,ka->ac', eris.fov, t1)
    Lac += 2*lib.einsum('kdac,kd->ac', eris.ovvv, t1)
    Lac -=   lib.einsum('kcad,kd->ac', eris.ovvv, t1)
    return Lac

### Eqs. (42)-(45) "chi"

def cc_Woooo(t1, t2, eris):
    lib = eris.lib
    Wklij = lib.einsum('kilc,jc->klij', eris.ooov, t1)
    Wklij += lib.einsum('ljkc,ic->klij', eris.ooov, t1)

    Wklij += lib.einsum('kcld,ijcd->klij', eris.ovov, t2)
    tmp    = lib.einsum('kcld,ic->kild', eris.ovov, t1)
    Wklij += lib.einsum('kild,jd->klij', tmp, t1)
    Wklij += eris.oooo.transpose(0,2,1,3)
    return Wklij

def cc_Wvvvv(t1, t2, eris):
    lib = eris.lib
    Wabcd  = lib.einsum('kdac,kb->abcd', eris.ovvv,-t1)
    Wabcd -= lib.einsum('kcbd,ka->abcd', eris.ovvv, t1)
    Wabcd += eris.vvvv.transpose(0,2,1,3)
    return Wabcd

def cc_Wvoov(t1, t2, eris):
    lib = eris.lib
    Wakic  = lib.einsum('kcad,id->akic', eris.ovvv, t1)
    Wakic -= lib.einsum('likc,la->akic', eris.ooov, t1)
    Wakic += eris.ovvo.transpose(2,0,3,1)

    Wakic -= 0.5*lib.einsum('ldkc,ilda->akic', eris.ovov, t2)
    Wakic -= 0.5*lib.einsum('lckd,ilad->akic', eris.ovov, t2)
    tmp    = lib.einsum('ldkc,id->likc', eris.ovov, t1)
    Wakic -= lib.einsum('likc,la->akic', tmp, t1)
    Wakic += lib.einsum('ldkc,ilad->akic', eris.ovov, t2)
    return Wakic

def cc_Wvovo(t1, t2, eris):
    lib = eris.lib
    Wakci  = lib.einsum('kdac,id->akci', eris.ovvv, t1)
    Wakci -= lib.einsum('kilc,la->akci', eris.ooov, t1)
    Wakci += eris.oovv.transpose(2,0,3,1)
    Wakci -= 0.5*lib.einsum('lckd,ilda->akci', eris.ovov, t2)
    tmp    = lib.einsum('lckd,la->ackd', eris.ovov, t1)
    Wakci -= lib.einsum('ackd,id->akci', tmp, t1)
    return Wakci

def Wooov(t1, t2, eris):
    lib = eris.lib
    Wklid  = lib.einsum('ic,kcld->klid', t1, eris.ovov)
    Wklid += eris.ooov.transpose(0,2,1,3)
    return Wklid

def Wvovv(t1, t2, eris):
    lib = eris.lib
    Walcd  = lib.einsum('ka,kcld->alcd',-t1, eris.ovov)
    Walcd += eris.ovvv.transpose(2,0,3,1)
    return Walcd

def W1ovvo(t1, t2, eris):
    lib = eris.lib
    Wkaci  = 2*lib.einsum('kcld,ilad->kaci', eris.ovov, t2)
    Wkaci +=  -lib.einsum('kcld,liad->kaci', eris.ovov, t2)
    Wkaci +=  -lib.einsum('kdlc,ilad->kaci', eris.ovov, t2)
    Wkaci += eris.ovvo.transpose(0,2,1,3)
    return Wkaci

def W2ovvo(t1, t2, eris):
    lib = eris.lib
    Wkaci = lib.einsum('la,lkic->kaci',-t1, Wooov(t1, t2, eris))
    Wkaci += lib.einsum('kcad,id->kaci', eris.ovvv, t1)
    return Wkaci

def Wovvo(t1, t2, eris):
    Wkaci = W1ovvo(t1, t2, eris) + W2ovvo(t1, t2, eris)
    return Wkaci

def W1ovov(t1, t2, eris):
    lib = eris.lib
    Wkbid = -lib.einsum('kcld,ilcb->kbid', eris.ovov, t2)
    Wkbid += eris.oovv.transpose(0,2,1,3)
    return Wkbid

def W2ovov(t1, t2, eris):
    lib = eris.lib
    Wkbid = lib.einsum('klid,lb->kbid', Wooov(t1, t2, eris),- t1)
    Wkbid += lib.einsum('kcbd,ic->kbid', eris.ovvv, t1)
    return Wkbid

def Wovov(t1, t2, eris):
    return W1ovov(t1, t2, eris) + W2ovov(t1, t2, eris)

def Woooo(t1, t2, eris):
    lib = eris.lib
    Wklij  = lib.einsum('kcld,ijcd->klij', eris.ovov, t2)
    tmp    = lib.einsum('kcld,ic->kild', eris.ovov, t1)
    Wklij += lib.einsum('kild,jd->klij', tmp, t1)
    Wklij += lib.einsum('kild,jd->klij', eris.ooov, t1)
    Wklij += lib.einsum('ljkc,ic->klij', eris.ooov, t1)
    Wklij += eris.oooo.transpose(0,2,1,3)
    return Wklij

def Wvvvv(t1, t2, eris):
    lib = eris.lib
    Wabcd  = lib.einsum('kcld,klab->abcd', eris.ovov, t2)
    tmp    = lib.einsum('kcld,ka->acld', eris.ovov, t1)
    Wabcd += lib.einsum('acld,lb->abcd', tmp, t1)
    Wabcd += eris.vvvv.transpose(0,2,1,3)
    Wabcd -= lib.einsum('ldac,lb->abcd', eris.ovvv, t1)
    Wabcd -= lib.einsum('kcbd,ka->abcd', eris.ovvv, t1)
    return Wabcd

def Wvvvo(t1, t2, eris, Wvvvv=None):
    lib = eris.lib
    Wabcj  =  -lib.einsum('alcj,lb->abcj', W1ovov(t1, t2, eris).transpose(1,0,3,2), t1)
    Wabcj +=  -lib.einsum('kbcj,ka->abcj', W1ovvo(t1, t2, eris), t1)
    Wabcj += 2*lib.einsum('ldac,ljdb->abcj', eris.ovvv, t2)
    Wabcj +=  -lib.einsum('ldac,ljbd->abcj', eris.ovvv, t2)
    Wabcj +=  -lib.einsum('lcad,ljdb->abcj', eris.ovvv, t2)
    Wabcj +=  -lib.einsum('kcbd,jkda->abcj', eris.ovvv, t2)
    Wabcj +=   lib.einsum('ljkc,lkba->abcj', eris.ooov, t2)
    tmp    =   lib.einsum('ljkc,lb->kcbj', eris.ooov, t1)
    Wabcj +=   lib.einsum('kcbj,ka->abcj', tmp, t1)
    Wabcj +=  -lib.einsum('kc,kjab->abcj', cc_Fov(t1, t2, eris), t2)
    Wabcj += eris.ovvv.transpose(3,1,2,0).conj()
    if Wvvvv is None:
        Wvvvv = Wvvvv(t1, t2, eris)
    Wabcj += lib.einsum('abcd,jd->abcj', Wvvvv, t1)
    return Wabcj

def Wovoo(t1, t2, eris):
    lib = eris.lib
    Wkbij  =   lib.einsum('kbid,jd->kbij', W1ovov(t1, t2, eris), t1)
    Wkbij +=  -lib.einsum('klij,lb->kbij', Woooo(t1, t2, eris), t1)
    Wkbij +=   lib.einsum('kbcj,ic->kbij', W1ovvo(t1, t2, eris), t1)
    Wkbij += 2*lib.einsum('kild,ljdb->kbij', eris.ooov, t2)
    Wkbij +=  -lib.einsum('kild,jldb->kbij', eris.ooov, t2)
    Wkbij +=  -lib.einsum('likd,ljdb->kbij', eris.ooov, t2)
    Wkbij +=   lib.einsum('kcbd,jidc->kbij', eris.ovvv, t2)
    tmp    =   lib.einsum('kcbd,ic->kibd', eris.ovvv, t1)
    Wkbij +=   lib.einsum('kibd,jd->kbij', tmp, t1)
    Wkbij +=  -lib.einsum('ljkc,libc->kbij', eris.ooov, t2)
    Wkbij +=   lib.einsum('kc,ijcb->kbij', cc_Fov(t1, t2, eris), t2)
    Wkbij += eris.ooov.transpose(1,3,0,2).conj()
    return Wkbij
