#ifndef __SOCKET_FDSET_H__
#define __SOCKET_FDSET_H__ 

////////////////////////////////////////////////////
//
//rhh
// This class needs to be broken into 2 classes: the gathering class and the processing functions.
// The functions should be set up as template functions
//
// Add a helper class socket_select. May want to totally separate the select and collect functionality
// fits more with the normal Berkeley mind set... ** Not ** Should think about using POLL() on BSD-based systems
//
//////////////////////////////////////////////////////////
#include "pandabase.h"
#include "numeric_types.h"
#include "time_base.h"
#include "socket_ip.h"

class Socket_fdset
{
PUBLISHED:
    
    inline Socket_fdset();
    inline void setForSocket(const Socket_IP &incon);
    inline bool IsSetFor(const Socket_IP & incon) const;
    inline int WaitForRead(bool zeroFds, PN_uint32 sleep_time = 0xffffffff);
    inline int WaitForWrite(bool zeroFds, PN_uint32 sleep_time = 0xffffffff);
    inline int WaitForError(bool zeroFds, PN_uint32 sleep_time = 0xffffffff);
    
    
    inline int WaitForRead(bool zeroFds, const Time_Span & timeout);
    inline void clear();
private:
    inline void setForSocketNative(const SOCKET inid);
    inline bool isSetForNative(const SOCKET inid) const;
    
    friend struct Socket_Selector;
    SOCKET _maxid;
    mutable fd_set _the_set;
};

////////////////////////////////////////////////////////////////////
// Function name : Socket_fdset::Socket_fdset
// Description   : The constructor
////////////////////////////////////////////////////////////////////
inline Socket_fdset::Socket_fdset()
{
    clear();
}

////////////////////////////////////////////////////////////////////
// Function name : Socket_fdset::setForSocketNative
// Description   : This does the physical manipulation of the set getting read for the base call
////////////////////////////////////////////////////////////////////
inline void Socket_fdset::setForSocketNative(SOCKET inid)
{
    assert( inid >= 0);
#ifndef WIN32
    assert(inid < FD_SETSIZE);
#endif
    
    FD_SET(inid, &_the_set);
    if (_maxid < inid)
        _maxid = inid;
}

////////////////////////////////////////////////////////////////////
// Function name : Socket_fdset::isSetForNative
// Description   :  Answer the question: was the socket marked for reading
//      there's a subtle difference in the NSPR version: it will respond if
//      the socket had an error
////////////////////////////////////////////////////////////////////
inline bool Socket_fdset::isSetForNative(SOCKET inid) const
{
    assert( inid >= 0);
#ifndef WIN32
    assert(inid < FD_SETSIZE);
#endif
    
    return (FD_ISSET(inid, &_the_set) != 0);
}

////////////////////////////////////////////////////////////////////
// Function name : Socket_fdset::IsSetFor
// Description   : check to see if a socket object has been marked for reading
////////////////////////////////////////////////////////////////////
inline bool Socket_fdset::IsSetFor(const Socket_IP & incon) const
{
    return isSetForNative(incon.GetSocket());
}

////////////////////////////////////////////////////////////////////
// Function name : WaitForRead
// Description   :
////////////////////////////////////////////////////////////////////
inline int Socket_fdset::WaitForRead(bool zeroFds, PN_uint32 sleep_time)
{
    int retVal = 0;
    if (sleep_time == 0xffffffff) 
    {
        retVal = DO_SELECT(_maxid + 1, &_the_set, NULL, NULL, NULL);
    }
    else 
    {
        timeval timeoutValue;
        timeoutValue.tv_sec = sleep_time / 1000;
        timeoutValue.tv_usec = (sleep_time % 1000) * 1000;
        
        retVal = DO_SELECT(_maxid + 1, &_the_set, NULL, NULL, &timeoutValue);
    }
    if (zeroFds)
        clear();
    
    return retVal;
}

//////////////////////////////////////////////////////////////
// Function name :  Socket_fdset::WaitForRead
// Description   :
//////////////////////////////////////////////////////////////
inline int Socket_fdset::WaitForRead(bool zeroFds, const Time_Span & timeout)
{
    timeval localtv = timeout.GetTval();
    
    int retVal = DO_SELECT(_maxid + 1, &_the_set, NULL, NULL, &localtv);
    if (zeroFds)
        clear();
    
    return retVal;
}

////////////////////////////////////////////////////////////////////
// Function name :  Socket_fdset::zeroOut
// Description   :  Marks the content as empty
////////////////////////////////////////////////////////////////////
inline void Socket_fdset::clear()
{
    _maxid = 0;
    FD_ZERO(&_the_set);
}

////////////////////////////////////////////////////////////////////
// Function name : Socket_fdset::setForSocket
// Description   :
////////////////////////////////////////////////////////////////////
inline void Socket_fdset::setForSocket(const Socket_IP &incon)
{
    setForSocketNative(incon.GetSocket());
}

////////////////////////////////
////////////////////////////////////////////////////////////////////
// Function name : Socket_fdset::WaitForWrite
// Description   : This is the function that will wait till
//      one of the sockets is ready for writing
////////////////////////////////////////////////////////////////////
inline int Socket_fdset::WaitForWrite(bool zeroFds, PN_uint32 sleep_time)
{
    int retVal = 0;
    if (sleep_time == 0xffffffff) 
    {
        retVal = DO_SELECT(_maxid + 1, NULL, &_the_set, NULL, NULL);
    }
    else 
    {
        timeval timeoutValue;
        timeoutValue.tv_sec = sleep_time / 1000;
        timeoutValue.tv_usec = (sleep_time % 1000) * 1000;
        
        retVal = DO_SELECT(_maxid + 1, NULL, &_the_set, NULL, &timeoutValue);
    }
    if (zeroFds)
        clear();
    
    return retVal;
}

//////////////////////////////////////////////////////////////
// Function name : Socket_fdset::WaitForError
// Description   : This is the function that will wait till
//      one of the sockets is in error state
//////////////////////////////////////////////////////////////
inline int Socket_fdset::WaitForError(bool zeroFds, PN_uint32 sleep_time)
{
    int retVal = 0;
    if (sleep_time == 0xffffffff) 
    {
        retVal = DO_SELECT(_maxid + 1, NULL, NULL, &_the_set, NULL);
    }
    else 
    {
        timeval timeoutValue;
        timeoutValue.tv_sec = sleep_time / 1000;
        timeoutValue.tv_usec = (sleep_time % 1000) * 1000;
        
        retVal = DO_SELECT(_maxid + 1, NULL, NULL, &_the_set, &timeoutValue);
    }
    if (zeroFds)
        clear();
    
    return retVal;
}


#endif //__SOCKET_FDSET_H__
