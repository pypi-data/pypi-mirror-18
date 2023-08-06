#ifndef INTERGRACIO_WINSHIT_H_   /* Include guard */
#define INTERGRACIO_WINSHIT_H_ 1

#if defined(_MSC_VER)

#define EXPORT(x) __declspec(dllexport) x
#define inline __inline

#if _MSC_VER < 1600
typedef          __int8         int8_t;
typedef          __int16        int16_t;
typedef          __int32        int32_t;
typedef          __int64        int64_t;

typedef unsigned __int8         uint8_t;
typedef unsigned __int16        uint16_t;
typedef unsigned __int32        uint32_t;
typedef unsigned __int64        uint64_t;
typedef unsigned __int64        size_t;
#else         // _MSC_VER >= 1600
#include <stdint.h>
#endif        // _MSC_VER < 1600

#else         // not defined(_MSC_VER) -> linux

#define EXPORT(x) x

#endif        // defined(_MSC_VER)

// usually on windows
#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif        // M_PI

#endif        // INTERGRACIO_WINSHIT_H_
