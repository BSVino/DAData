/*
Copyright (c) 2012, Lunar Workshop, Inc.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software must display the following acknowledgement:
   This product includes software developed by Lunar Workshop, Inc.
4. Neither the name of the Lunar Workshop nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY LUNAR WORKSHOP INC ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL LUNAR WORKSHOP BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#pragma once

#ifdef WITH_EASTL
#include <EASTL/vector.h>
#include <EASTL/heap.h>

#define TVECTOR_BASE eastl::vector<T>
using eastl::remove;
using eastl::find;
using eastl::push_heap;
using eastl::pop_heap;
using eastl::make_heap;
using eastl::sort_heap;
#else
#include <vector>
#include <algorithm>

#define TVECTOR_BASE std::vector<T>
using std::remove;
using std::find;
#endif

template <class T>
class tvector : public TVECTOR_BASE
{
public:
	inline tvector()
		: TVECTOR_BASE()
	{}

public:
	void erase_value(const T& value)
	{
		erase(remove(tvector<T>::begin(), tvector<T>::end(), value), tvector<T>::end());
	}

#ifndef WITH_EASTL
	using TVECTOR_BASE::push_back;

	T& push_back()
	{
		TVECTOR_BASE::push_back(T());
		return TVECTOR_BASE::back();
	}

	void set_capacity(size_t n = ~0)
	{
		size_t iSize = TVECTOR_BASE::size();
		if((n == ~0) || (n <= iSize))
		{
			if(n < iSize)
				TVECTOR_BASE::resize(n);

			tvector temp(*this); 
			swap(temp);
		}
		else
		{
			TVECTOR_BASE::resize(n);
			TVECTOR_BASE::resize(iSize);
		}
	}
#endif
};
